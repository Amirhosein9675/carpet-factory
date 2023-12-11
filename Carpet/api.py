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
    page_size = 10
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

            existing_record = ServiceProviders.objects.filter(
                national_code=request.data['national_code'] or '',
                phone_number=request.data['phone_number'] or ''
            ).first()
            print(existing_record)

            if existing_record:
                return Response({'status': 'Record with the same national_code or phone_number already exists'},
                                status=status.HTTP_400_BAD_REQUEST)

            service_p = ServiceProviders()
            service_p.first_name = request.data['first_name']
            service_p.last_name = request.data['last_name']
            service_p.phone_number = request.data['phone_number']
            service_p.address = request.data['address']
            service_p.national_code = request.data['national_code']
            service_p.save()
            #if len(request.data['services']) > 0:
            if len(json.loads(request.data['services'])) > 0:
                #list_services = request.data['services']
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
    
    def validate_phone_number(self, value):
        # Check if a driver with the same phone number already exists
        if Driver.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A driver with this phone number already exists.")
        return value

    def validate_national_code(self, value):
        # Check if a driver with the same national code already exists
        if Driver.objects.filter(national_code=value).exists():
            raise serializers.ValidationError("A driver with this national code already exists.")
        return value

    def validate_car_number(self, value):
        # Check if a driver with the same car number already exists
        if Driver.objects.filter(car_number=value).exists():
            raise serializers.ValidationError("A driver with this car number already exists.")
        return value


class ServiceCreate(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class TransferCarpet(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = []
            transfers = Transfer.objects.all()
            print(len(request.query_params))
            print(dict(request.GET))
            # services_param = request.query_params.get('services').split(',')
            # print(len(services_param))
            if len(request.query_params) > 0:
                params = dict(request.GET)
                # print(params['services'])
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

                for key in params:
                    params[key] = params[key][0]
                print(params)
                transfers = transfers.filter(**params)

            for transfer in transfers:
                print(transfer)

                serializer = GetTransferSerializers(transfer)
                print(serializer.data)
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

    # def perform_create(self, serializer):
    #     # Add a print statement to debug
    #     print("Performing create operation")
    #     serializer.save()


class TestTransferUpdateView(UpdateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class TransferPartialUpdateView(APIView):
    def patch(self, request, pk):
        transfer = Transfer.objects.get(pk=pk)
        serializer = TransferPartialUpdateSerializer(
            transfer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TransferListAPIView(ListAPIView):
#     serializer_class = TransferSerializer
#     queryset = Transfer.objects.all()
#     pagination_class = CustomPagination  # Use your custom pagination class

#     def get_queryset(self):
#         class TransferManager(models.Manager):
#             def filter_transfers(manager_self, status=None, service_provider=None, worker=None, carpets=None, services=None, start_date=None, end_date=None):
#                 filters = {}
#                 if status is not None:
#                     filters['status'] = status
#                 if service_provider is not None:
#                     filters['service_provider'] = service_provider
#                 if worker is not None:
#                     filters['worker'] = worker
#                 if carpets is not None:
#                     filters['carpets__in'] = carpets
#                 if services is not None:
#                     filters['services__id__exact'] = services
#                 if start_date is not None:
#                     filters['date__gte'] = start_date
#                 if end_date is not None:
#                     filters['date__lte'] = end_date

#                 return Transfer.objects.filter(**filters)

#         manager = TransferManager()

#         # Get parameters from the request
#         status = self.request.query_params.get('status', None)
#         service_provider = self.request.query_params.get('service_provider', None)
#         worker = self.request.query_params.get('worker', None)
#         carpets = self.request.query_params.getlist('carpets', None)
#         services = self.request.query_params.getlist('services', None)
#         start_date = self.request.query_params.get('start_date', None)
#         end_date = self.request.query_params.get('end_date', None)

#         # Convert carpet and service IDs to actual objects
#         carpet_objects = models.Carpet.objects.filter(id__in=carpets) if carpets else None
#         service_objects = models.Service.objects.filter(id__in=services) if services else None

#         # Filter transfers based on parameters
#         queryset = manager.filter_transfers(
#             status=status,
#             service_provider=service_provider,
#             worker=worker,
#             carpets=carpet_objects,
#             services=service_objects,
#             start_date=start_date,
#             end_date=end_date
#         )

#         return queryset


class TransferManager(models.Manager):
    def filter_transfers(self, status=None, service_provider=None, worker=None, carpets=None, services=None, start_date=None, end_date=None):
        filters = {}

        if status is not None:
            filters['status'] = status

        if service_provider is not None:
            filters['service_provider'] = service_provider

        if worker is not None:
            filters['worker'] = worker

        if carpets is not None:
            try:
                carpet_ids = [int(carpet_id) for carpet_id in carpets.split(',')]
                filters['carpets__id__in'] = carpet_ids
            except ValueError:
                raise Http404("Invalid carpet ID provided.")

        if services is not None:
            try:
                service_ids = [int(service_id) for service_id in services.split(',')]
                filters['services__id__in'] = service_ids
            except ValueError:
                raise Http404("Invalid service ID provided.")

        if start_date is not None:
            filters['date__gte'] = start_date

        if end_date is not None:
            filters['date__lte'] = end_date

        return Transfer.objects.filter(**filters)


class TransferListAPIView(ListAPIView):
    serializer_class = TransferSerializer
    queryset = Transfer.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        manager = TransferManager()

        # Get parameters from the request
        status = self.request.query_params.get('status', None)
        service_provider = self.request.query_params.get('service_provider', None)
        worker = self.request.query_params.get('worker', None)
        carpets = self.request.query_params.get('carpets', None)
        services = self.request.query_params.get('services', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        # Set the default end time to 23:59:59 if end_date is provided without time
        if end_date and len(end_date) == 10:
            end_date += "T23:59:59"

        # Filter transfers based on parameters
        try:
            queryset = manager.filter_transfers(
                status=status,
                service_provider=service_provider,
                worker=worker,
                carpets=carpets,
                services=services,
                start_date=start_date,
                end_date=end_date
            )
        except Http404 as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return queryset