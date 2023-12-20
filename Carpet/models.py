from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.title


class ServiceProviders(models.Model):
    first_name = models.CharField(max_length=256, blank=False, null=False)
    last_name = models.CharField(max_length=256, blank=False, null=False)
    phone_number = models.CharField(max_length=256,null=False, blank=False)
    address = models.TextField(null=True, blank=True)
    national_code = models.CharField(max_length=256,null=True, blank=True)
    services = models.ManyToManyField(Service)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class Driver(models.Model):
    first_name = models.CharField(max_length=256, blank=False, null=False)
    last_name = models.CharField(max_length=256, blank=False, null=False)
    phone_number = models.CharField(max_length=256,null=False, blank=False)
    national_code = models.CharField(max_length=256,null=True, blank=True)
    car = models.CharField(max_length=256, null=True, blank=True)
    car_number = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class Carpet(models.Model):
    factory = models.CharField(max_length=256, null=True, blank=True)
    barcode = models.CharField(max_length=256,null=False, blank=False)
    map_code = models.CharField(max_length=256)
    size = models.CharField(max_length=128)
    color = models.CharField(max_length=128)
    costumer_name = models.CharField(max_length=256, null=True, blank=True)
    kind=models.CharField(max_length=256,null=True,blank=True)
    density=models.CharField(max_length=256,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.barcode)


class Status(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.title


class Transfer(models.Model):
    carpets = models.ManyToManyField(Carpet, related_name='transfers')
    status = models.ForeignKey(
        Status, blank=True, null=True, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(
        ServiceProviders, on_delete=models.CASCADE,null=True,blank=True)
    services = models.ManyToManyField(Service)
    worker = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    admin_verify = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.is_finished and self.admin_verify:
            return "تایید نهایی"
        elif self.is_finished != True  and self.admin_verify !=True:
            return "عدم تایید کارگر و ادمین"
        elif self.is_finished == True  and self.admin_verify !=True:
            return "عدم تایید ادمین"
        else:
            return"نامشخص"
            
class Statistics(models.Model):
    service=models.ForeignKey(Service,on_delete=models.CASCADE)
    kind=models.CharField(max_length=256,blank=False,null=False)
    size=models.CharField(max_length=256,blank=False,null=False)
    custom_size=models.IntegerField()
    
    def __str__(self) -> str:
        return self.kind

  