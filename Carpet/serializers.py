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
        fields = ['id', 'first_name', 'last_name', 'services',
                  'phone_number', 'address', 'national_code']


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


class DriverListSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


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
            if field_name in [field.name for field in Transfer._meta.get_fields()]:
                field = getattr(instance, field_name)
                if hasattr(field, 'add'):
                    field.set(value)
                else:
                    setattr(instance, field_name, value)
            else:
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


class UserUpdatePatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class StatusUpdatePatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = "__all__"


class ServiceUpdatePatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class ServiceProviderUpdatePatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceProviders
        fields = "__all__"

    def validate(self, data):

        phone_number = data.get('phone_number')
        if phone_number and ServiceProviders.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Phone number already exists.")

        national_code = data.get('national_code')
        if national_code and ServiceProviders.objects.filter(national_code=national_code).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("National code already exists.")

        return data


class DriverUpdatePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"

    def validate(self, data):

        phone_number = data.get('phone_number')
        if phone_number and Driver.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Phone number already exists.")

        national_code = data.get('national_code')
        if national_code and Driver.objects.filter(national_code=national_code).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("National code already exists.")

        car_number = data.get('car_number')
        if car_number and Driver.objects.filter(car_number=car_number).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Car number already exists.")

        return data


class CarpetUpdatePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpet
        fields = "__all__"


class StatisticsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statistics
        fields = "__all__"


class StatisticsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statistics
        fields = "__all__"


class StatisticsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statistics
        fields = "__all__"


class TransferwithCarpetSerializer(serializers.ModelSerializer):

    def get_services(self, obj):
        data = []
        service_obj = {}
        for service in obj.services.all():
            service_obj = {}
            service_obj['id'] = service.id
            service_obj['title'] = service.title
            data.append(service_obj)
        return data

    def get_service_provider(self, obj):
        if obj.service_provider is not None:
            data = []
            service_provider_obj = {}
            service_provider_obj['id'] = obj.service_provider.id
            service_provider_obj['first_name'] = obj.service_provider.first_name
            service_provider_obj['last_name'] = obj.service_provider.last_name
            service_provider_obj['phone_number'] = obj.service_provider.phone_number
            service_provider_obj['address'] = obj.service_provider.address
            service_provider_obj['national_code'] = obj.service_provider.national_code
            data.append(service_provider_obj)
            return data
        else:
            return None

    def get_worker(self, obj):
        if obj.worker is not None:
            data = []
            worker_obj = {}
            worker_obj['id'] = obj.worker.id
            worker_obj['first_name'] = obj.worker.first_name
            worker_obj['last_name'] = obj.worker.last_name
            data.append(worker_obj)
            return data
        else:
            return None

    services = serializers.SerializerMethodField("get_services")
    service_provider = serializers.SerializerMethodField(
        "get_service_provider")
    worker = serializers.SerializerMethodField("get_worker")

    class Meta:
        model = Transfer
        fields = ['id', 'status', 'date', 'is_finished',
                  'admin_verify', 'service_provider', 'worker', 'services']


class CarpetwithTransferSerializer(serializers.ModelSerializer):

    transfers = TransferwithCarpetSerializer(many=True, read_only=True)

    class Meta:
        model = Carpet
        fields = ['id','factory','barcode','map_code','size','color','costumer_name','kind','density','transfers']

class LastTransferSerializer(serializers.ModelSerializer):
    def get_services(self, obj):
        data = []
        service_obj = {}
        for service in obj.services.all():
            service_obj = {}
            service_obj['id'] = service.id
            service_obj['title'] = service.title
            data.append(service_obj)
        return data
    
    def get_service_provider(self, obj):
        if obj.service_provider is not None:
            data = []
            service_provider_obj = {}
            service_provider_obj['id'] = obj.service_provider.id
            service_provider_obj['first_name'] = obj.service_provider.first_name
            service_provider_obj['last_name'] = obj.service_provider.last_name
            service_provider_obj['phone_number'] = obj.service_provider.phone_number
            service_provider_obj['address'] = obj.service_provider.address
            service_provider_obj['national_code'] = obj.service_provider.national_code
            data.append(service_provider_obj)
            return data
        else:
            return None
        
    def get_worker(self, obj):
        if obj.worker is not None:
            data = []
            worker_obj = {}
            worker_obj['id'] = obj.worker.id
            worker_obj['first_name'] = obj.worker.first_name
            worker_obj['last_name'] = obj.worker.last_name
            data.append(worker_obj)
            return data
        else:
            return None
    def get_carpets(self,obj):
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
            carpet_obj['kind'] = carpet.kind
            carpet_obj['density'] = carpet.density
            data.append(carpet_obj)
        return data
    
    carpets = serializers.SerializerMethodField("get_carpets")
    worker = serializers.SerializerMethodField("get_worker") 
    services = serializers.SerializerMethodField("get_services")
    service_provider = serializers.SerializerMethodField("get_service_provider")
    
    
    class Meta:
        model = Transfer
        fields = "__all__"