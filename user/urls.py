from django.urls import path
from .views import CustomerSignUpView, AddAddress

app_name = 'user'

urlpatterns = [
    path('customer-signup', CustomerSignUpView.as_view(), name='customer-signup'),
    path('add-address', AddAddress.as_view(), name='add-address'),
]
