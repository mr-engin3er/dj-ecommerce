from django.urls import path
from .views import add_to_cart, remove_from_cart

app_name = 'order'
urlpatterns = [
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),

]
