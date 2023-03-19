from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discounted_price', 'slug')
    readonly_fields = ['slug']


admin.site.register(Product, ProductAdmin)
