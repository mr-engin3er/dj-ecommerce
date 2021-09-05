from django import forms
from order.models import State, City


class CheckoutForm(forms.Form):
    ADDRESS_CHOICES = (('HOME', 'Home'),
                       ('OFFICE', 'Office'))
    PAYMENT_CHOICES = (('STRIPE', 'Credit/Debit Cards'),
                       ('NET-BANKING', 'Net Banking'),
                       ('UPI', 'UPI'))

    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Full name', 'id': 'address', 'class': 'form-control'
    }))
    mobile_number = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Mobile number', 'id': 'mobile', 'class': 'form-control'
    }))
    house_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'House number', 'id': 'house', 'class': 'form-control'
    }))
    street_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Street name', 'id': 'street', 'class': 'form-control'
    }))
    colony = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Colony', 'id': 'colony', 'class': 'form-control'
    }))
    landmark = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Landmark(eg. Hospital, School etc.)', 'id': 'landmark', 'class': 'form-control'
    }))
    state = forms.ModelChoiceField(queryset=State.objects.all(), widget=forms.Select(attrs={
        'placeholder': 'Select State', 'id': 'state', 'class': 'custom-select d-block w-100'
    }))
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs={
        'placeholder': 'Select City', 'id': 'city', 'class': 'custom-select d-block w-100'
    }))
    pin_code = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Pin code', 'id': 'pincode', 'class': 'form-control'
    }))
    default_address = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'default_address', 'class': 'custom-control-input',
    }))
    address_type = forms.ChoiceField(choices=ADDRESS_CHOICES,
                                     widget=forms.RadioSelect())
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES,
                                       widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(
                    state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['city'].queryset = self.instance.state.city_set.order_by(
        #         'name')
