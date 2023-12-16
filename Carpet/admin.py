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


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['service','kind','size','custom_size']

admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceProviders, ServiceProviderAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Carpet, CarpetAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Transfer) 
admin.site.register(Statistics,StatisticsAdmin)
