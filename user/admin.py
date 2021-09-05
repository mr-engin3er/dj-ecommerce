from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Customer
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'last_login']
    exclude = ['password']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender']

    def user(self, instance):
        try:
            return instance.user.email
        except ObjectDoesNotExist:
            return "ERROR!"


admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
