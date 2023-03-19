import json
import stripe
import random
import string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from order.models import Order, ProductInCart, ReturnOrder
from user.models import Customer
from payment.forms import CouponForm, RefundForm
from .models import Coupon, Payment


# Get secret key from env
stripe.api_key = settings.STRIPE_SECRET_KEY

# Get webhook secret
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


def create_order_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))


class PaymentView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        if order.shipping_address:
            amount = order.get_cart_total()
            stripe_amount = order.stripe_price()
            context = {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
                       "amount": amount,
                       "stripe_amount": stripe_amount
                       }
            return render(self.request, "payment.html", context)
        messages.warning(request, "Can't checkout without address.")
        return redirect("order:checkout")


# stripe intent view for custom form checkout
class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        # get customer input
        req_json = json.loads(request.body)
        # create or get stripe customer
        customer_user = Customer.objects.get(user=request.user)
        if customer_user.payment_id:
            payment_id = customer_user.payment_id
            customer = stripe.Customer.retrieve(payment_id)
        else:
            customer = stripe.Customer.create(email=req_json['email'])
            customer_user.payment_id = customer['id']
            customer_user.save()
        amount = req_json['amount']

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='inr',
                payment_method_types=['card'],
                customer=customer['id'],
                metadata={
                    "total": amount,
                    "user": request.user.email
                }
            )
            # redirect to success url
            messages.success(request, "Payment Successfull")
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.warning(request, f"{err.get('messages')}")
            return JsonResponse({'error': str(e)})

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(request, "Rate Limit Error")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(request, "Invalid request error")
            return JsonResponse({'error': str(e)})

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(request, "Not Authenticated")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(request, "Network error")
            return JsonResponse({'error': str(e)})

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                request, "Something went wrong. You were not charged. Please try again")
            return JsonResponse({'error': str(e)})

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            # send an email to ourselves
            print(e)
            messages.warning(
                request, "A serious error occurred. We have been notified")
            return JsonResponse({'error': str(e)})


def success(request):
    return render(request, "payment-success.html")

# stripe webhook to get event while payment


@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # try to get event otherwise raise error
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('value error in webhook', e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('Signature Verification Error in webhook', e)
        return HttpResponse(status=400)

    # if payment successful and checkout session completed send email to customer
    if event['type'] == 'checkout.session.completed':
        # grab session from event which was started by create-checkout-session
        session = event['data']['object']

        # Fulfill the purchase...
        # fulfill_order(session)
        # grab customer email from session
        customer_email = session['customer_details']['email']

        # grab product id from metadata of session which was sent by checkout page
        # product_id = session['metadata']['product_id']
        # product = Product.objects.get(id=product_id)

        # send email to customer
        send_mail(
            subject="Thanks for purchase",
            # {product.get_url()}
            message=f"Here is Your product, Product url is ",
            recipient_list=[customer_email, ],
            from_email="test@admin.com"
        )
    elif event["type"] == "payment_intent.succeeded":
        # grab intent from event which was created by create-payment-intent
        intent = event['data']['object']

        print(intent["metadata"])

        user_model = get_user_model()
        user = user_model.objects.get(email=intent["metadata"]["user"])

        # create payment entry in database
        order = Order.objects.get(user=user, ordered=False)
        payment = Payment()
        payment.stripe_charge_id = intent['id']
        payment.user = user
        payment.amount = order.get_cart_total()
        payment.save()

        # fullfill order
        order.ordered = True
        order.payment = payment
        order.order_id = create_order_id()
        order.save()
        product_qs = ProductInCart.objects.filter(
            user=user, ordered=False).order_by('id')
        product_qs.update(ordered=True)

        # grab stripe customer from intent
        stripe_customer_id = intent['customer']
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']

        # grab product from metadata of intent which was sent by create-payment-intent view
        # product_id = intent["metadata"]["product_id"]
        # product = Product.objects.get(id=product_id)

        # send email to customer
        send_mail(
            subject="Here is your product",
            # {product.get_url()}
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is ",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

    # Passed signature verification
    return HttpResponse(status=200)


def __get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.warning(request, "Invalid coupon code.", extra_tags="danger")


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=request.user, ordered=False)
                order.coupon = __get_coupon(request, code)
                order.save()
                messages.warning(request, "Successfully added coupon.",
                                 extra_tags="success")
                return redirect("order:checkout")
            except ObjectDoesNotExist:
                messages.warning(request, "You don't have any order.",
                                 extra_tags="danger")
                return redirect("order:checkout")
    messages.warning(request, "Something went wrong!",
                     extra_tags="danger")
    return redirect("order:checkout")


def return_request(request):
    if request.method == 'POST':
        form = RefundForm(request.POST or None)
        if form.is_valid():
            order_id = form.cleaned_data.get('order_id')
            message = form.cleaned_data.get('message')
            try:
                order = Order.objects.get(order_id=order_id)
                order.refund_requested = True
                order.save()
                return_order = ReturnOrder()
                return_order.order = order
                return_order.reason = message
                return_order.save()
                messages.info(
                    request, "You've requested for return. We'll notify you by Email.", extra_tags='info')
                return redirect('payment:return-request')
            except ObjectDoesNotExist:
                messages.warning(
                    request, "Order not found for return.", extra_tags='info')
                return redirect('payment:return-request')

    form = RefundForm()
    context = {
        'form': form
    }
    return render(request, 'return_request.html', context)
