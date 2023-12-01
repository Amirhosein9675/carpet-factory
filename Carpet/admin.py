from django.contrib import admin
from .models import *

# Register your models here.


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title']


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number']


class DriverAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number']


class CarpetAdmin(admin.ModelAdmin):
    list_display = ['factory', 'barcode', 'map_code', 'size', 'color']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['title']


#class TransferAdmin(admin.ModelAdmin):
   # list_display = ['is_finished', 'admin_verify']


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceProviders, ServiceProviderAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Carpet, CarpetAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Transfer) #TransferAdmin)
