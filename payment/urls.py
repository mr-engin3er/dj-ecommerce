from django.urls import path
from .views import (
    PaymentView,
    StripeIntentView,
    stripe_webhook,
    success
)

app_name = 'payment'
urlpatterns = [
    path("<payment_option>/", PaymentView.as_view(), name="index"),
    path("create-payment-intent", StripeIntentView.as_view(),
         name="create-payment-intent"),
    path("hooks", stripe_webhook, name="hooks"),
    path("success", success, name="success")

]
