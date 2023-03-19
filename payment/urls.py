from django.urls import path
from .views import (
    PaymentView,
    StripeIntentView,
    stripe_webhook,
    success,
    add_coupon,
    return_request
)

app_name = 'payment'
urlpatterns = [
    path("option/<payment_option>/", PaymentView.as_view(), name="option"),
    path("create-payment-intent", StripeIntentView.as_view(),
         name="create-payment-intent"),
    path('add-coupon/', add_coupon, name='add-coupon'),
    path("hooks", stripe_webhook, name="hooks"),
    path("success", success, name="success"),
    path("return-request", return_request, name="return-request")

]
