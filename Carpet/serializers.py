from rest_framework import serializers
from .models import Service, ServiceProviders
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
    def get_user(self,obj):
        user_obj={}
        user_obj['id']=obj.user.id
        user_obj['first_name']=obj.user.first_name
        user_obj['last_name']=obj.user.last_name
        return user_obj
    
            
            
        


    services = serializers.SerializerMethodField("get_services")
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ServiceProviders
        fields = "__all__"
