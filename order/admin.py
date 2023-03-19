from django.contrib import admin
from .models import ProductInCart, Order, ReturnOrder
# Register your models here.


def make_refund_request_granted(modeladmin, request, queryset):
    queryset.update(refund_granted=True)


make_refund_request_granted.short_description = 'Update to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_id', 'ordered', 'delivered', 'refund_requested',
                    'refund_granted']
    list_filter = ['ordered', 'delivered', 'refund_requested',
                   'refund_granted']
    readonly_fields = ['order_id']
    search_fields = ['user__email', 'order_id']
    actions = [make_refund_request_granted]


admin.site.register(ProductInCart)
admin.site.register(Order, OrderAdmin)
admin.site.register(ReturnOrder)
