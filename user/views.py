from django.contrib import messages
from django.views.generic.base import View
from user.models import User, Address
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import AddressForm, CustomerSignUpForm
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


class AddAddress(View):
    def get(self, request, *args, **kwargs):
        form = AddressForm()
        context = {
            "form": form
        }
        return render(request, 'add_address.html', context)

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST or None)
        if form.is_valid():
            full_name = form.cleaned_data.get(
                'full_name')
            mobile_number = form.cleaned_data.get(
                'mobile_number')
            house_number = form.cleaned_data.get(
                'house_number')
            street_name = form.cleaned_data.get(
                'street_name')
            colony = form.cleaned_data.get('colony')
            landmark = form.cleaned_data.get('landmark')
            state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            pin_code = form.cleaned_data.get('pin_code')
            address_type = form.cleaned_data.get('address_type')
            default = form.cleaned_data.get('default')

            address = Address(
                user=request.user,
                full_name=full_name,
                mobile_number=mobile_number,
                house_number=house_number,
                street_name=street_name,
                colony=colony,
                landmark=landmark,
                state=state,
                city=city,
                pin_code=pin_code,
                address_type=address_type,
                default_address=default
            )
            if default:
                qs = Address.objects.filter(user=request.user)
                qs.update(default_address=False)
            address.save()
            messages.success(request, "Address added successfully")
            return redirect("/")
