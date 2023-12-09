from rest_framework import serializers
from .models import *
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model

# class CustomUserDetailsSerializer(UserDetailsSerializer):
#     is_staff = serializers.SerializerMethodField()

#     class Meta(UserDetailsSerializer.Meta):
#         model = get_user_model()
#         fields = ('pk', 'username', 'email', 'is_staff', 'first_name','last_name',)
#         print("777777")

#     def get_is_staff(self, obj):
#         return obj.is_staff


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

    def get_worker(self, obj):
        data = []
        worker_obj = {}
        worker_obj['id'] = obj.worker.id
        worker_obj['first_name'] = obj.worker.first_name
        worker_obj['last_name'] = obj.worker.last_name
        data.append(worker_obj)
        return data

    def get_service_provider(self, obj):
        data = []
        print(80*'-')
        print(obj)
        service_provider_obj = {}
        service_provider_obj['id'] = obj.service_provider.id
        service_provider_obj['first_name'] = obj.service_provider.first_name
        service_provider_obj['last_name'] = obj.service_provider.last_name
        data.append(service_provider_obj)
        return data

    def get_status(self, obj):
        data = []
        status_obj = {}
        status_obj['id'] = obj.status.id
        status_obj['title'] = obj.status.title

        data.append(status_obj)
        return data
    carpets = serializers.SerializerMethodField("get_carpets")
    services = serializers.SerializerMethodField("get_services")
    worker = serializers.SerializerMethodField("get_worker")
    service_provider = serializers.SerializerMethodField(
        "get_service_provider")
    status = serializers.SerializerMethodField("get_status")

    class Meta:
        model = Transfer
        fields = "__all__"


# teeeeestttttttt
class CarpetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpet
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class ServiceProvidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviders
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TransferSerializer(serializers.ModelSerializer):
   
        carpets = serializers.PrimaryKeyRelatedField(many=True, queryset=Carpet.objects.all(), required=False)
        status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), allow_null=True, required=False)
        service_provider = serializers.PrimaryKeyRelatedField(queryset=ServiceProviders.objects.all(), allow_null=True, required=False)
        services = serializers.PrimaryKeyRelatedField(many=True, queryset=Service.objects.all(), required=False)
        worker = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
        
        class Meta:
            
            model = Transfer
            fields = '__all__'
    
        
class TransferPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

    def update(self, instance, validated_data):
        for field_name, value in validated_data.items():
            # Check if the field is a ManyToManyField
            if field_name in [field.name for field in Transfer._meta.get_fields()]:
                field = getattr(instance, field_name)
                if hasattr(field, 'add'):  # Check if it's a many-to-many field
                    # Use add() for ManyToManyField
                    field.set(value)
                else:
                    # For other fields, update directly
                    setattr(instance, field_name, value)
            else:
                # Handle other fields not defined in the model if needed
                pass

        instance.save()
        return instance

class TransferSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
