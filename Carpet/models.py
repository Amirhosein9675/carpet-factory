from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.title


class ServiceProviders(models.Model):
    first_name = models.CharField(max_length=256, blank=False, null=False)
    last_name = models.CharField(max_length=256, blank=False, null=False)
    phone_number = models.BigIntegerField(null=False, blank=False)
    address = models.TextField(null=True, blank=True)
    national_code = models.BigIntegerField(null=True, blank=True)
    services = models.ManyToManyField(Service)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class Driver(models.Model):
    first_name = models.CharField(max_length=256, blank=False, null=False)
    last_name = models.CharField(max_length=256, blank=False, null=False)
    phone_number = models.BigIntegerField(null=False, blank=False)
    national_code = models.BigIntegerField(null=True, blank=True)
    car = models.CharField(max_length=256, null=True, blank=True)
    car_number = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class Carpet(models.Model):
    factory = models.CharField(max_length=256, null=True, blank=True)
    barcode = models.BigIntegerField(null=False, blank=False)
    map_code = models.CharField(max_length=256)
    size = models.CharField(max_length=128)
    color = models.CharField(max_length=128)
    costumer_name = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.barcode)


class Status(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.title


class Transfer(models.Model):
    carpets = models.ManyToManyField(Carpet)
    status = models.OneToOneField(Status, on_delete=models.CASCADE)
    service_privider = models.ForeignKey(
        ServiceProviders, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    worker = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)
    admin_veryfy = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.status.title

    @property
    def valid_services(self):
        valid_services = []
        for service in self.services:
            if service in self.service_privider['services']:
                valid_services.append(service)
        return valid_services
