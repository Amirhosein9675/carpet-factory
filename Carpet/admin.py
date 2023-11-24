from django.contrib import admin
from .models import *

# Register your models here.


class Adminadmin(admin.ModelAdmin):
    list_display = ['user']


class WorkerAdmin(admin.ModelAdmin):
    list_display = ['user']


class ServiceProvidersAdmin(admin.ModelAdmin):
    list_display = ['user']


class DriverAdmin(admin.ModelAdmin):
    list_display = ['user']


class CarpetFctoryAdmin(admin.ModelAdmin):
    list_display = ['title']


class CarpetAdmin(admin.ModelAdmin):
    list_display = ['title', 'barcode', 'owner']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_activate']


admin.site.register(Admin, Adminadmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(ServiceProviders, ServiceProvidersAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(CarpetFactory, CarpetFctoryAdmin)
admin.site.register(Service)
admin.site.register(Carpet, CarpetAdmin)
admin.site.register(Status)
