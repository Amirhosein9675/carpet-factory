from rest_framework import serializers
from .models import *
from django.core.validators import int_list_validator
from rest_framework.fields import ListField


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, max_length=128, allow_null=False, allow_blank=False)
    password = serializers.CharField(
        required=True, max_length=256, allow_null=False, allow_blank=False)
    firstname = serializers.CharField(
        required=True, max_length=128, allow_null=False, allow_blank=False)
    lastname = serializers.CharField(
        required=True, max_length=128, allow_null=False, allow_blank=False)
    p_number = serializers.IntegerField(required=True, allow_null=False)
    roole = serializers.CharField(required=True, allow_null=False)


class GetServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class UpdateServiceProvidersSerializer(serializers.ModelSerializer):
    # s_providersid=serializers.IntegerField(required=True, allow_null=False)
    # services1=serializers.ListField(child=serializers.IntegerField(),allow_empty=True, required=False)

    class Meta:
        model = ServiceProviders
        fields = "__all__"


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

    def get_user(self, obj):
        user_obj = {}
        user_obj['id'] = obj.user.id
        user_obj['first_name'] = obj.user.first_name
        user_obj['last_name'] = obj.user.last_name
        return user_obj

    services = serializers.SerializerMethodField("get_services")
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ServiceProviders
        fields = "__all__"


class GetCarpetSerializer(serializers.ModelSerializer):

    def get_owner(self, obj):
        owner_obj = {}
        owner_obj['id'] = obj.owner.id
        owner_obj['title'] = obj.owner.title
        return owner_obj

    def get_status(self, obj):
        status_obj = {}
        status_obj['id'] = obj.status.id
        status_obj['title'] = obj.status.title
        return status_obj

    def get_service_provider(self, obj):
        service_provider_obj = {}
        service_provider_obj['id'] = obj.service_provider.user.id
        service_provider_obj['first_name'] = obj.service_provider.user.first_name
        service_provider_obj['last_name'] = obj.service_provider.user.last_name
        return service_provider_obj

    owner = serializers.SerializerMethodField("get_owner")
    status = serializers.SerializerMethodField("get_status")
    service_provider = serializers.SerializerMethodField(
        "get_service_provider")

    class Meta:
        model = Carpet
        fields = "__all__"
        
class GetStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"
