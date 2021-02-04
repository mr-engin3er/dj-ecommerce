from django.shortcuts import render
from django.views.generic.list import ListView
from product.models import Product
# Create your views here.


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    paginate_by = 12
