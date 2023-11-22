from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Service(models.Model):
    title=models.CharField(max_length=256)
    
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


class ServiceProviders(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False)
    phone_number = models.TextField(null=False, blank=False)
    services=models.ManyToManyField(Service)
    
    

    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False)
    phone_number = models.TextField(null=False, blank=False)

    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name
class CarpetFactory(models.Model):
    title=models.CharField(max_length=256,null=False,blank=False)
    carpet_id=models.BigIntegerField(null=False,blank=False)
    
    def __str__(self) -> str:
        return self.title
