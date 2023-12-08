from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework import serializers
from .serializers import *
import json
from datetime import datetime
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination
from django_filters.rest_framework import DjangoFilterBackend


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page = 1
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'page'


class RegisterUser(APIView):
    def post(self, request, format=None):
        try:
            for item in list(request.data.keys()):
                if item not in ['username', 'password', 'firstname', 'lastname', 'is_staff']:
                    return Response({'status': f'key {item} is wrong'}, status=status.HTTP_400_BAD_REQUEST)

            seria = RegisterUserSerializer(data=request.data)

            if seria.is_valid():
                username = seria.data.get('username')
                password = seria.data.get('password')
                firstname = seria.data.get('firstname')
                lastname = seria.data.get('lastname')
                is_staff = seria.data.get('is_staff')
            else:
                return Response({'status': 'bad request serializer not valid'}, status=status.HTTP_400_BAD_REQUEST)
            for valid_user in User.objects.all():
                if valid_user.username == username:
                    return Response({'status': f'username,{username} allready exsit'}, status=status.HTTP_400_BAD_REQUEST)

            user_new = User()
            user_new.username = username
            user_new.password = password
            user_new.first_name = firstname
            user_new.last_name = lastname
            user_new.is_staff = is_staff
            user_new.save()

            return Response({'status': 'okkk'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'internal service error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceproviderList(ListAPIView):
    queryset = ServiceProviders.objects.all()
    serializer_class = GetServiceProviderSerializer


class ServiceproviderCreate(APIView):
    def post(self, request, format=None):
        try:
            for item in list(request.data.keys()):
                if item not in ['first_name', 'last_name', 'phone_number', 'address', 'national_code', 'services']:
                    return Response({'status': f'key {item} is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            service_p = ServiceProviders()
            service_p.first_name = request.data['first_name']
            service_p.last_name = request.data['first_name']
            service_p.phone_number = request.data['phone_number']
            service_p.address = request.data['address']
            service_p.national_code = request.data['national_code']
            service_p.save()
            # if len(request.data['services']) > 0:
            if len(json.loads(request.data['services'])) > 0:
                # list_services = request.data['services']
                list_services = json.loads(request.data['services'])
                for services_item in list_services:
                    service = Service.objects.get(id=services_item)
                    service_p.services.add(service)
            else:
                return Response({'status': 'field services can not null'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCarpet(ListAPIView):
    queryset = Carpet.objects.all()
    serializer_class = GetCarpetSerializer


class CarpetDetails(APIView):
    def get(self, request, pk, format=None):
        try:
            carpet = Carpet.objects.get(id=pk)
            carpet_serializer = CarpetDetailSerializer(carpet, many=False)
            return Response({'data': carpet_serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CarpetFromExcel(APIView):
    def post(self, request, format=None):
        try:
            for item in list(request.data.keys()):
                if item not in ['factory', 'barcode', 'map_code', 'size', 'color', 'costumer_name']:
                    return Response({'status': f'key {item} is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            seria = CarpetDetailSerializer(data=request.data)
            if seria.is_valid():
                factory = seria.data.get('factory')
                barcode = seria.data.get('barcode')
                map_code = seria.data.get('map_code')
                size = seria.data.get('size')
                color = seria.data.get('color')
                costumer_name = seria.data.get('costumer_name')
            else:
                return Response({'status': 'bad request serializer not valid'}, status=status.HTTP_400_BAD_REQUEST)
            carpet_new = Carpet()
            carpet_new.factory = factory
            carpet_new.barcode = barcode
            carpet_new.map_code = map_code
            carpet_new.size = size
            carpet_new.color = color
            carpet_new.costumer_name = costumer_name
            carpet_new.save()

            return Response({'status': 'carpet object saved successfully'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostTransfer(APIView):
    def create_transfer_necesary_fileds(self, data):
        print(80*'$')
        print(len(data['worker']))
        if len(data['worker']) > 0:
            print('amiiiir')
            worker = User.objects.get(id=data['worker'])
        if len(data['service_provider']) > 0:
            service_provider = ServiceProviders.objects.get(
                id=data['service_provider'])
        date_string = data['date']
        format = "%Y/%m/%d %H:%M:%S"
        date = datetime.strptime(date_string, format)
        fields = {"date": date}
        print(fields)
        print(80*'+')
        return fields

    def create_transfer(self, data, transfer):
        print(80*'=')
        transfer.is_finished = data['is_finished']
        transfer.admin_verify = data['admin_verify']
        status = Status.objects.get(id=data['status'])
        transfer.status = status
        print(transfer)
        print(80*'/')
        transfer.save()
        print(80*'&')

        if len(json.loads(data['carpet'])) > 0:
            # if len(data['carpet']) > 0:
            # carpet_barcode = data['carpet'][0]
            carpet_barcode = json.loads(data['carpet'])[0]
            print(carpet_barcode)
            print(80*'f')
            carpet = Carpet.objects.get(barcode=carpet_barcode)
            transfer.carpets.add(carpet)
        # if len(data['services']) > 0:
        if len(json.loads(data['services'])) > 0:
            # list_services = data['services']
            list_services = json.loads(data['services'])
            for services_item in list_services:
                service = Service.objects.get(id=services_item)
                transfer.services.add(service)
        print(80*'()')
        # print(json.loads(data['services']))
        # print(type(json.loads(data['services'])))

    def post(self, request, format=None):
        try:
            for item in list(request.data.keys()):
                if item not in ['carpet', 'status', 'service_provider', 'services', 'worker', 'date', 'is_finished', 'admin_verify']:
                    return Response({'status': f'key {item} is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            if len(request.data['worker']) and len(request.data['service_provider']):
                self.create_transfer(request.data, Transfer(worker=self.create_transfer_necesary_fileds(request.data)['worker'],
                                                            service_provider=self.create_transfer_necesary_fileds(request.data)[
                    'service_provider'],
                    date=self.create_transfer_necesary_fileds(request.data)['date']))
            else:
                self.create_transfer(request.data, Transfer(
                    date=self.create_transfer_necesary_fileds(request.data)['date']))

            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTransfer(ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = GetTransferSerializers
    pagination_class = CustomPagination


class UpdateTransfer(PostTransfer, APIView):
    def post(self, request, format=None):
        try:
            for item in list(request.data.keys()):
                if item not in ['id', 'carpet', 'status', 'service_provider', 'services', 'worker', 'date', 'is_finished', 'admin_verify']:
                    return Response({'status': f'key {item} is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            trans = Transfer.objects.get(id=request.data['id'])
            # trans.delete()
            print(80*'*')
            PostTransfer.create_transfer(self, request.data, trans)
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateTransferByDRF(UpdateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = UpdateAgain1serializer


class GetServices(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = GetServicesSerializer


class UpdateServiceProviders(APIView):
    def post(self, request):
        try:
            print(request.data)
            print(request.data['id'])
            services = json.loads(request.data['services1'])
            print(services)
            service_p = ServiceProviders.objects.filter(
                id=request.data['id'])

            for service in services:
                print(service['id'])
                t = Service.objects.get(id=service['id'])
                for field in service_p:
                    field.services.add(t)
            return Response({'status': 'okk'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetStatus(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = GetStatusSerializer


class UpdateCarpet(APIView):
    def post(self, request):
        try:
            staus_upadat = Status.objects.get(id=request.data['status_id'])
            for item in list(request.data.keys()):
                if item not in ['status_id', 'carpet_id']:
                    return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

            print(request.data['status_id'])
            print(staus_upadat)
            carpet = Carpet.objects.filter(
                id=request.data['carpet_id']).update(status=staus_upadat)
            return Response({'status': 'okk'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserDetail(ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserDetailSerializer


# class TransferPage(ListAPIView):
#     queryset = Transfer.objects.all()
#     serializer_class = GetTransferSerializers
#     pagination_class = PageNumberPagination


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserListSerializer


class DriverList(ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverListSerializer


class DriverCreate(CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverListSerializer


class TransferCarpet(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = []
            transfers = Transfer.objects.all()
            print(len(request.query_params))
            print(dict(request.GET))
            #services_param = request.query_params.get('services').split(',')
            #print(len(services_param))
            params = dict(request.GET)
            #print(params['services'])
            if "services" in params.keys():
                services_param = request.query_params.get(
                    'services').split(',')
                if services_param[0] != '':
                    for service in services_param:
                        transfers = transfers.filter(services=service)
                print(params['services'])
                print(services_param)
                params.pop('services')
            if "carpets" in params.keys():
                carpets_barcode_params = request.query_params.get(
                    'carpets').split(',')
                if carpets_barcode_params[0] != '':
                    for carpet_barcode in carpets_barcode_params:
                        transfers = transfers.filter(
                            carpets__barcode=carpet_barcode)
                print(params['carpets'])
                print(carpets_barcode_params)
                params.pop('carpets')
            if "dates" in params.keys():
                dates_param = request.query_params.get('dates').split(',')
                if dates_param[0] != '':
                    transfers = transfers.filter(date__range=dates_param)
                    print(dates_param)
                params.pop('dates')
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            #for key in params:
                #params[key] = params[key][0]
            #print(params)
            transfers = transfers.filter(**params)
            
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            
            for transfer in transfers:
                serializer = TransferCarpetSerializers(transfer)
                data.append(serializer.data)
            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransferCarpet2(ListAPIView):

    queryset = Transfer.objects.all()
    serializer_class = TransferCarpetSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['services']

    def get_queryset(self):
        services = self.request.query_params.get('services').split(',')
        print(services)
        d = self.queryset.filter(services__in=services)
        print(len(d))
        return self.queryset.filter(services__in=services)

# #get kole userha //
# get va poste hame rannde //
# get va poste service provider//
# get hme transfer ==>
# get hame farsh ha ==>filterha:id midi joziat migiri,barcode midi to transfer etlat migiri

# filters = {
#     key: value
#     for key, value in request.post.items()
#     if key in ['filter1', 'filter2', 'filter3']
# }

# Test.objects.filter(**filters)


class TestCreateTransfer(CreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def perform_create(self, serializer):
        # Add a print statement to debug
        print("Performing create operation")
        serializer.save()
