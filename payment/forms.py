from django import forms


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
                           'class': 'form-control', 'placeholder': 'Promo code',
                           'aria-label': "Recipient's username", "aria-describedby": "basic-addon2"}))


class RefundForm(forms.Form):
    order_id = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
