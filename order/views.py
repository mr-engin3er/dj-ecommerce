from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View
from django.http import Http404
from product.models import Product
from .forms import CheckoutForm
from .models import Order, ProductInCart, State, City, Address
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
            messages.error(request, "You don't have an active order.")
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
        form = CheckoutForm()
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(request, 'checkout.html', context)

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST or None)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            if form.is_valid():
                full_name = form.cleaned_data.get('full_name')
                mobile_number = form.cleaned_data.get('mobile_number')
                house_number = form.cleaned_data.get('house_number')
                street_name = form.cleaned_data.get('street_name')
                colony = form.cleaned_data.get('colony')
                landmark = form.cleaned_data.get('landmark')
                state = form.cleaned_data.get('state')
                city = form.cleaned_data.get('city')
                pin_code = form.cleaned_data.get('pin_code')
                address_type = form.cleaned_data.get('address_type')
                default_address = form.cleaned_data.get('default_address')
                payment_method = form.cleaned_data.get('payment_method')

                address = Address(
                    user=request.user,
                    full_name=full_name,
                    mobile_number=mobile_number,
                    house_number=house_number,
                    street_name=street_name,
                    colony=colony,
                    landmark=landmark,
                    state=state,
                    city=city,
                    pin_code=pin_code,
                    address_type=address_type,
                    default_address=default_address
                )
                address.save()
                order.address = address
                order.save()
                if payment_method == 'STRIPE':
                    return redirect('payment:index', payment_option="stripe")
                elif payment_method == 'NET-BANKING':
                    return redirect('payment:index', payment_option="stripe")
                if payment_method == 'UPI':
                    return redirect('payment:index', payment_option="stripe")
                else:
                    messages.warning(request, "Invalid Payment Option")
                return redirect("/")

            messages.warning(request, "You do not have an active order")
            return redirect("order:checkout")
        except ObjectDoesNotExist:
            messages.error(request, "You don't have an active order.")
            return redirect("/")


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})
