from django.urls import path
from .views import CustomerSignUpView

app_name = 'user'

urlpatterns = [
    path('customer-signup', CustomerSignUpView.as_view(), name='customer-signup')
]
