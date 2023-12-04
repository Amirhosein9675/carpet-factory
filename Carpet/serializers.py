from rest_framework import serializers
from .models import *


class RegisterUserSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True, max_length=128, allow_null=False, allow_blank=False)
    password = serializers.CharField(
        required=True, max_length=256, allow_null=False, allow_blank=False)
    firstname = serializers.CharField(
        required=True, max_length=128, allow_null=False, allow_blank=False)
    lastname = serializers.CharField(
        required=True, max_length=128, allow_null=False, allow_blank=False)
    is_staff = serializers.BooleanField(required=True)

    # class Meta:
    #     model = User
    #     fields = ['username', 'password',
    #               'first_name', 'last_name', 'is_staff']


class GetServiceProviderSerializer(serializers.ModelSerializer):

    def get_services(self, obj):
        data = []
        service_obj = {}
        for service in obj.services.all():
            service_obj = {}
            service_obj['id'] = service.id
            service_obj['title'] = service.title
            data.append(service_obj)
        return data

    # def get_user(self, obj):
    #     user_obj = {}
    #     user_obj['id'] = obj.user.id
    #     user_obj['first_name'] = obj.user.first_name
    #     user_obj['last_name'] = obj.user.last_name
    #     return user_obj

    services = serializers.SerializerMethodField("get_services")
    # user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ServiceProviders
        fields = ['id', 'first_name', 'last_name', 'services']


class CarpetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carpet
        fields = ['id', 'barcode']


class CarpetDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carpet
        fields = "__all__"


class GetServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class UpdateServiceProvidersSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceProviders
        fields = "__all__"


class GetCarpetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carpet
        fields = "__all__"


class GetStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"


class GetUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'is_staff', 'is_active', 'email']


class GetUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class GetTransferSerializers(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = "__all__"


class UpdateAgain1serializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = "__all__"


class DriverListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = "__all__"


class Services_pSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class CreateServiceProviderSerializer(serializers.ModelSerializer):
    services = Services_pSerializer(many=True)

    class Meta:
        model = ServiceProviders
        # fields="__all__"
        fields = ['first_name', 'last_name', 'phone_number',
                  'address', 'national_code', 'services']


class TransferCarpetSerializers(serializers.ModelSerializer):

    def get_carpets(self, obj):
        data = []
        carpet_obj = {}
        for carpet in obj.carpets.all():
            carpet_obj = {}
            carpet_obj['id'] = carpet.id
            carpet_obj['factory'] = carpet.factory
            carpet_obj['barcode'] = carpet.barcode
            carpet_obj['map_code'] = carpet.map_code
            carpet_obj['size'] = carpet.size
            carpet_obj['color'] = carpet.color
            carpet_obj['costumer_name'] = carpet.costumer_name
            data.append(carpet_obj)
        return data
    
    def get_services(self, obj):
        data = []
        service_obj = {}
        for service in obj.services.all():
            service_obj = {}
            service_obj['id'] = service.id
            service_obj['title'] = service.title
            data.append(service_obj)
        return data
    
    def get_worker(self,obj):
        data=[]
        worker_obj={}
        worker_obj['id']=obj.worker.id
        worker_obj['first_name']=obj.worker.first_name
        worker_obj['last_name']=obj.worker.last_name
        data.append(worker_obj)
        return data
        
    carpets = serializers.SerializerMethodField("get_carpets")
    services = serializers.SerializerMethodField("get_services")
    worker = serializers.SerializerMethodField("get_worker")


    class Meta:
        model = Transfer
        fields = "__all__"
