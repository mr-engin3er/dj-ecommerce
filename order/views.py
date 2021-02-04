from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from product.models import Product
from .models import Order, OrderInCart
# Create your views here.


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    add_product_to_cart, created = OrderInCart.objects.get_or_create(
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


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user
    )
    if order_qs.exists():
        order = order_qs[0]
        print(order)
        # check if the order item is in the order
        if order.product.filter(product__slug=product.slug):
            order_in_cart = OrderInCart.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.product.remove(order_in_cart)
            messages.warning(
                request, "Product removed from your cart", extra_tags='danger')
        else:
            # TODO: add message user dont contain product in cart
            messages.warning(
                request, "You don't have this product in your cart", extra_tags='danger')
            return redirect('product:product', slug=slug)
    else:
        # TODO: add message user dont have order
        messages.warning(
            request, "You don't have this product in your cart", extra_tags='danger')
        return redirect('product:product', slug=slug)

    return redirect('product:product', slug=slug)
