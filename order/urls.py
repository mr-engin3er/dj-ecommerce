from django.urls import path
from .views import (
    add_to_cart,
    load_cities,
    remove_from_cart,
    CartSummeryView,
    CheckoutView,
    add_single_product_to_cart,
    remove_single_product_from_cart,
)

app_name = 'order'
urlpatterns = [
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-single-product-to-cart/<slug>/',
         add_single_product_to_cart, name='add-single-product-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-product-from-cart/<slug>/',
         remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('cart-summery/', CartSummeryView.as_view(), name='cart-summery'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('load-cities/', load_cities, name='load-cities'),

]
