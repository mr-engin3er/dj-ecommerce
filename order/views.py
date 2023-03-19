from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View
from product.models import Product
from payment.forms import CouponForm
from user.models import City, Address
from .forms import CheckoutForm
from .models import Order, ProductInCart
# Create your views here.


class CartSummeryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'order': order,
            }
            return render(request, 'cart_summery.html', context)
        except ObjectDoesNotExist:
            messages.warning(request, "You don't have an active order.")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    add_product_to_cart, created = ProductInCart.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.product.filter(product__slug=product.slug).exists():
            add_product_to_cart.quantity += 1
            add_product_to_cart.save()
            messages.info(request, 'product quantity was updated successfully')
        else:
            messages.info(request, 'product added to cart successfully')
            order.product.add(add_product_to_cart)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date,)
        messages.info(request, 'product added to cart successfully')
        order.product.add(add_product_to_cart)
    return redirect('product:product', slug=slug)


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.product.filter(product__slug=product.slug).exists():
            product_in_cart = ProductInCart.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.product.remove(product_in_cart)
            product_in_cart.delete()
            if order.product.count() == 0:
                order.delete()
            messages.warning(
                request, "Product removed from your cart", extra_tags='danger')
            return redirect('order:cart-summery')

        else:
            messages.warning(
                request, "You don't have this product in your cart", extra_tags='danger')
            return redirect('product:product', slug=slug)
    else:
        messages.warning(
            request, "You don't have this product in your cart", extra_tags='danger')
        return redirect('product:product', slug=slug)


@login_required
def add_single_product_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    add_product_to_cart = ProductInCart.objects.get(
        product=product,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.product.filter(product__slug=product.slug).exists():
            add_product_to_cart.quantity += 1
            add_product_to_cart.save()
            messages.info(request, 'product quantity was updated successfully')
        else:
            messages.info(request, 'product added to cart successfully')
            # order.product.add(add_product_to_cart)
    else:
        # ordered_date = timezone.now()
        # order = Order.objects.create(
        #     user=request.user, ordered_date=ordered_date,)
        messages.info(request, 'product added to cart successfully')
        # order.product.add(add_product_to_cart)
    return redirect('order:cart-summery')


@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.product.filter(product__slug=product.slug).exists():
            product_in_cart = ProductInCart.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if product_in_cart.quantity > 1:
                product_in_cart.quantity -= 1
                product_in_cart.save()
                messages.warning(
                    request, "Product quanyity is updated", extra_tags='danger')
            else:
                order.product.remove(product_in_cart)
                product_in_cart.delete()
                if order.product.count() == 0:
                    order.delete()
                messages.warning(
                    request, "Product removed from your cart", extra_tags='danger')
        else:
            messages.warning(
                request, "You don't have this product in your cart", extra_tags='danger')
            return redirect('order:cart-summery')

    else:
        messages.warning(
            request, "You don't have this product in your cart", extra_tags='danger')
        return redirect('order:cart-summery')
    return redirect('order:cart-summery')


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        form = CheckoutForm()
        coupon = CouponForm()
        context = {
            'form': form,
            'order': order,
            'coupon': coupon
        }
        addresses = Address.objects.filter(
            user=request.user)
        context.update({"addresses": addresses})
        return render(request, 'checkout.html', context)

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST or None)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            print('-------> form', form.data)
            if form.is_valid():
                shipping_address = form.cleaned_data.get('shipping_address')
                print('-------- form.cleaned_data', form.cleaned_data)
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')
                if same_billing_address:
                    billing_address = shipping_address
                else:
                    billing_address = form.cleaned_data.get('billing_address')

                payment_method = form.cleaned_data.get('payment_method')

                order.shipping_address = Address.objects.get(
                    id=shipping_address)
                order.billing_address = Address.objects.get(id=billing_address)

                order.save()
                if payment_method == 'STRIPE':
                    return redirect('payment:option', payment_option="stripe")
                elif payment_method == 'NET-BANKING':
                    return redirect('payment:option', payment_option="stripe")
                if payment_method == 'UPI':
                    return redirect('payment:option', payment_option="stripe")
                else:
                    messages.warning(request, "Invalid Payment Option")
                return redirect("/")

            messages.warning(request, "You do not have an active order")
            return redirect("order:checkout")
        except ObjectDoesNotExist:
            messages.warning(request, "You don't have an active order.")
            return redirect("/")


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})
