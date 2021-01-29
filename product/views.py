from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Product
# Create your views here.


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'
