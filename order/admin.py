from django.contrib import admin
from .models import OrderInCart, Order, State, City, Address
# Register your models here.

admin.site.register(OrderInCart)
admin.site.register(Order)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Address)
