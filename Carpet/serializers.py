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


class GetUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class GetUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'is_staff', 'is_active', 'email']


class GetServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def validate_title(self, value):

        if Service.objects.filter(title=value).exists():
            raise serializers.ValidationError(
                "A Service with this title already exists.")
        return value


class GetCarpetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carpet
        fields = "__all__"


class CarpetDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carpet
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

    services = serializers.SerializerMethodField("get_services")

    class Meta:
        model = ServiceProviders
        fields = ['id', 'first_name', 'last_name', 'services']


class DriverListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = "__all__"

    def validate_phone_number(self, value):
        # Check if a driver with the same phone number already exists
        if Driver.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "A driver with this phone number already exists.")
        return value

    def validate_national_code(self, value):
        # Check if a driver with the same national code already exists
        if Driver.objects.filter(national_code=value).exists():
            raise serializers.ValidationError(
                "A driver with this national code already exists.")
        return value

    def validate_car_number(self, value):
        # Check if a driver with the same car number already exists
        if Driver.objects.filter(car_number=value).exists():
            raise serializers.ValidationError(
                "A driver with this car number already exists.")
        return value


class GetStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"


class TransferSerializer(serializers.ModelSerializer):

    carpets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Carpet.objects.all(), required=False)
    status = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), allow_null=True, required=False)
    service_provider = serializers.PrimaryKeyRelatedField(
        queryset=ServiceProviders.objects.all(), allow_null=True, required=False)
    services = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Service.objects.all(), required=False)
    worker = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False)

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
        fields = "__all__"


class DestroyTransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = "__all__"


class DestroyCarpetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carpet
        fields = "__all__"


class DestroyDriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = "__all__"


class DestroyServiceProvidersSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceProviders
        fields = "__all__"


class DestroyServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class DestroyStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"


class DestroyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class AdminVerifyTransferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transfer
        fields = "__all__"

class WorkerTransferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transfer
        fields = "__all__"