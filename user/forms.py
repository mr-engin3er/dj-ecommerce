from .models import Customer, User, State, City
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


GENDER_CHOICES = (('MALE', 'Male'),
                  ('FEMALE', 'Female'))


class CustomerSignUpForm(UserCreationForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["first_name", "last_name", "email"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.gender = self.cleaned_data.get('gender')
        customer.save()
        return user


class AddressForm(forms.Form):
    ADDRESS_CHOICES = ((1, 'Home'),
                       (2, 'Office'))
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Full name', 'id': 'full_name', 'class': 'form-control'
    }))
    mobile_number = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Mobile number', 'id': 'mobile_number', 'class': 'form-control'
    }))
    house_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'House number', 'id': 'house_number', 'class': 'form-control'
    }))
    street_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Street name', 'id': 'street_name', 'class': 'form-control'
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
        'placeholder': 'Pin code', 'id': 'pin_code', 'class': 'form-control'
    }))
    address_type = forms.ChoiceField(choices=ADDRESS_CHOICES,
                                     widget=forms.RadioSelect())
    default = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'default', 'class': 'custom-control-input',
    }))

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
