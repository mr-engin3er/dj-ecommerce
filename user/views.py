from user.models import User
from django.contrib.auth import models
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import CustomerSignUpForm
# Create your views here.


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'user/customer-signup.html'

    def get_context_data(self, **kwargs):
        # kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user,
              backend='allauth.account.auth_backends.AuthenticationBackend')
        return redirect('home:home')
