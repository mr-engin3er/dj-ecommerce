from django.contrib import admin
from .models import ProductInCart, Order, State, City, Address
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']


admin.site.register(ProductInCart)
admin.site.register(Order, OrderAdmin)
admin.site.register(State)
admin.site.register(City, CityAdmin)
admin.site.register(Address)
