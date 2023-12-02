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
    # s_providersid=serializers.IntegerField(required=True, allow_null=False)
    # services1=serializers.ListField(child=serializers.IntegerField(),allow_empty=True, required=False)

    class Meta:
        model = ServiceProviders
        fields = "__all__"


class GetCarpetSerializer(serializers.ModelSerializer):

    # def get_owner(self, obj):
    #     owner_obj = {}
    #     owner_obj['id'] = obj.owner.id
    #     owner_obj['title'] = obj.owner.title
    #     return owner_obj

    # def get_status(self, obj):
    #     status_obj = {}
    #     status_obj['id'] = obj.status.id
    #     status_obj['title'] = obj.status.title
    #     return status_obj

    # def get_service_provider(self, obj):
    #     service_provider_obj = {}
    #     service_provider_obj['id'] = obj.service_provider.user.id
    #     service_provider_obj['first_name'] = obj.service_provider.user.first_name
    #     service_provider_obj['last_name'] = obj.service_provider.user.last_name
    #     return service_provider_obj

    # owner = serializers.SerializerMethodField("get_owner")
    # status = serializers.SerializerMethodField("get_status")
    # service_provider = serializers.SerializerMethodField(
    #     "get_service_provider")

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


class GetUserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class GetTransferSerializers(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = "__all__"


# # class TransferSerializer(serializers.ModelSerializer, serializers.Serializer):
# #     # carpet_barcode = json.loads(data['carpet'])[0]
# #     # carpet = Carpet.objects.get(barcode=carpet_barcode)
# #     # transfer.carpets.add(carpet)

# #     # list_services = json.loads(data['services'])
# #     # for services_item in list_services:
# #     #     service = Service.objects.get(id=services_item)
# #     #     transfer.services.add(service)

# #     carpets = serializers.ManyRelatedField(Carpet)
# #     status = serializers.On(
# #         Status, blank=True, null=True, on_delete=models.CASCADE)
# #     service_provider = serializers.ForeignKey(
# #         ServiceProviders, on_delete=models.CASCADE)
# #     services = serializers.ManyToManyField(Service)
# #     worker = models.ForeignKey(User, on_delete=models.CASCADE)
# #     date = serializers.DateTimeField()
# #     is_finished = serializers.BooleanField(default=False)
# #     admin_verify = serializers.BooleanField(default=False)

# #     def update(self, instance, validated_data):
# #         """
# #         Update and return an existing `Snippet` instance, given the validated data.
# #         """
# #         instance.worker = validated_data.get('worker', instance.worker)
# #         instance.service_provider = validated_data.get(
# #             'service_provider', instance.service_provider)
# #         instance.services = validated_data.get('services', instance.services)
# #         instance.is_finished = validated_data.get(
# #             'is_finished', instance.is_finished)
# #         instance.status = validated_data.get('status', instance.status)
# #         instance.admin_verify = validated_data.get(
# #             'admin_verify', instance.admin_verify)
# #         instance.carpet = validated_data.get('carpet', instance.carpet)
# #         instance.date = validated_data.get('date', instance.date)

#         instance.save()
#         return instance

class UpdateAgain1serializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = "__all__"
