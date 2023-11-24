from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.title


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False)
    phone_number = models.TextField(null=False, blank=False)

    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False)
    phone_number = models.TextField(null=False, blank=False)

    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name


class ServiceProviders(models.Model):  # pak k
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False)
    phone_number = models.TextField(null=False, blank=False)
    services = models.ManyToManyField(Service, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False)
    phone_number = models.TextField(null=False, blank=False)

    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name


class CarpetFactory(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self) -> str:
        return self.title


class Carpet(models.Model):
    title = models.CharField(max_length=256, null=False, blank=False)
    barcode = models.BigIntegerField(null=False, blank=False)
    owner = models.ForeignKey(CarpetFactory, on_delete=models.CASCADE)
    status = models.ForeignKey(
        'Status', on_delete=models.CASCADE, null=False, blank=False)
    service_provider=models.OneToOneField(ServiceProviders,on_delete=models.CASCADE,null=True,blank=True)
    

    def __str__(self) -> str:
        return self.title


class Status(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    #is_activate = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
