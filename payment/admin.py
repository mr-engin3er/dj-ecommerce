from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Payment, Coupon
# Register your models here.


class PaymentAdmin(ModelAdmin):
    readonly_fields = ['stripe_charge_id']
    list_display = ['user', 'stripe_charge_id', 'amount']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Coupon)
