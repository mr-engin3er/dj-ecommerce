from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Customer, Address, State, City
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


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'default_address', 'address_type', 'state', 'city']
    list_filter = ['state', 'city']
    search_fields = ['user__email',  'state__name', 'city__name']


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']


admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(State)
admin.site.register(City, CityAdmin)
