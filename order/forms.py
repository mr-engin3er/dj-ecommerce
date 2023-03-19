from django import forms
from user.models import Address


class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = (('STRIPE', 'Credit/Debit Cards'),
                       ('NET-BANKING', 'Net Banking'),
                       ('UPI', 'UPI'))

    same_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'same_billing_address', 'class': 'custom-control-input',
    }))

    shipping_address = forms.CharField()
    billing_address = forms.CharField()
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES,
                                       widget=forms.RadioSelect())
