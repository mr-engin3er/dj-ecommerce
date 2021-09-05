from user.models import Customer, User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import models
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
