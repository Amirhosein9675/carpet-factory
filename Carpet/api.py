from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework import serializers
from .serializers import *
import json
from django.http import Http404
from rest_framework import pagination


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


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserListSerializer


class GetUserDetail(ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserDetailSerializer


class GetServices(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = GetServicesSerializer


class ServiceCreate(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


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


class UpdateCarpet(APIView):
    def post(self, request):
        try:
            staus_upadat = Status.objects.get(id=request.data['status_id'])
            for item in list(request.data.keys()):
                if item not in ['status_id', 'carpet_id']:
                    return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
            carpet = Carpet.objects.filter(
                id=request.data['carpet_id']).update(status=staus_upadat)
            return Response({'status': 'okk'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateServiceProviders(APIView):
    def post(self, request):
        try:
            services = json.loads(request.data['services1'])
            service_p = ServiceProviders.objects.filter(
                id=request.data['id'])
            for service in services:
                t = Service.objects.get(id=service['id'])
                for field in service_p:
                    field.services.add(t)
            return Response({'status': 'okk'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class DriverList(ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverListSerializer


class DriverCreate(CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverListSerializer


class GetStatus(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = GetStatusSerializer

# class TransferManager(models.Manager):
#     def filter_transfers(self, status=None, service_provider=None, worker=None, carpets=None, services=None, start_date=None, end_date=None):
#         filters = {}

#         if status is not None:
#             filters['status'] = status

#         if service_provider is not None:
#             filters['service_provider'] = service_provider

#         if worker is not None:
#             filters['worker'] = worker

#         if carpets is not None:
#             try:
#                 carpet_ids = [int(carpet_id) for carpet_id in carpets.split(',')]
#                 filters['carpets__id__in'] = carpet_ids
#             except ValueError:
#                 raise Http404("Invalid carpet ID provided.")

#         if services is not None:
#             try:
#                 service_ids = [int(service_id) for service_id in services.split(',')]
#                 filters['services__id__in'] = service_ids
#             except ValueError:
#                 raise Http404("Invalid service ID provided.")

#         if start_date is not None:
#             filters['date__gte'] = start_date

#         if end_date is not None:
#             filters['date__lte'] = end_date

#         return Transfer.objects.filter(**filters)

# class TransferListAPIView(ListAPIView):
#     serializer_class = TransferSerializer
#     queryset = Transfer.objects.all()
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         manager = TransferManager()

#         # Get parameters from the request
#         status = self.request.query_params.get('status', None)
#         service_provider = self.request.query_params.get('service_provider', None)
#         worker = self.request.query_params.get('worker', None)
#         carpets = self.request.query_params.get('carpets', None)
#         services = self.request.query_params.get('services', None)
#         start_date = self.request.query_params.get('start_date', None)
#         end_date = self.request.query_params.get('end_date', None)

#         # Set the default end time to 23:59:59 if end_date is provided without time
#         if end_date and len(end_date) == 10:
#             end_date += "T23:59:59"

#         # Filter transfers based on parameters
#         try:
#             queryset = manager.filter_transfers(
#                 status=status,
#                 service_provider=service_provider,
#                 worker=worker,
#                 carpets=carpets,
#                 services=services,
#                 start_date=start_date,
#                 end_date=end_date
#             )
#         except Http404 as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         return queryset


class TransferPartialUpdateView(APIView):
    def patch(self, request, pk):
        transfer = Transfer.objects.get(pk=pk)
        serializer = TransferPartialUpdateSerializer(
            transfer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class TestCreateTransfer(CreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer




# teeeeeeeest


class TransferManager(models.Manager):
    def filter_transfers(self, status=None, service_provider=None, worker=None, carpets=None, services=None, start_date=None, end_date=None, **carpet_filters):
        filters = {}

        if status is not None:
            filters['status'] = status

        if service_provider is not None:
            filters['service_provider'] = service_provider

        if worker is not None:
            filters['worker'] = worker

        if carpets is not None:
            try:
                carpet_ids = carpets
                filters['carpets__id__in'] = carpet_ids
            except Http404 as e:
                raise e  # Propagate the Http404 exception

        if services is not None:
            try:
                service_ids = [int(service_id)
                               for service_id in services.split(',')]
                filters['services__id__in'] = service_ids
            except ValueError:
                raise Http404("Invalid service ID provided.")

        if start_date is not None:
            filters['date__gte'] = start_date

        if end_date is not None:
            filters['date__lte'] = end_date

        return Transfer.objects.filter(**filters)

    def filter_carpet_ids(self, **carpet_filters):
        # Initialize with all carpet IDs
        print(80*'-')
        carpet_ids = Carpet.objects.values_list('id', flat=True)
        print(carpet_ids)
        # Add filters for all Carpet model fields
        carpet_fields = [field.name for field in Carpet._meta.get_fields(
        ) if isinstance(field, models.CharField)]
        print(carpet_fields)
        for field in carpet_fields:
            value = carpet_filters.get(field, None)
            if value is not None:
                carpet_ids = Carpet.objects.filter(
                    **{field: value, 'id__in': carpet_ids}).values_list('id', flat=True)

        if not carpet_ids:
            raise Http404("No matching carpet records found.")
        carpet_ids=list(carpet_ids)
        #print(type(carpet_ids))
        return carpet_ids


class TransferListAPIView(ListAPIView):
    serializer_class = TransferSerializer1
    queryset = Transfer.objects.all()
    # You need to define CustomPagination or use another pagination class
    pagination_class = CustomPagination
    manager = TransferManager()

    def get_queryset(self):
        # Get parameters from the request
        status = self.request.query_params.get('status', None)
        service_provider = self.request.query_params.get(
            'service_provider', None)
        worker = self.request.query_params.get('worker', None)
        # carpets = self.request.query_params.get('carpets', None)
        services = self.request.query_params.get('services', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        print(services)
        # Set the default end time to 23:59:59 if end_date is provided without time
        if end_date and len(end_date) == 10:
            end_date += "T23:59:59"

        try:
            # Instead of directly using carpet IDs, you can use filter_carpet_ids
            carpet_ids = self.manager.filter_carpet_ids(
                # Add more Carpet model fields as needed
                factory=self.request.query_params.get('factory', None),
                barcode=self.request.query_params.get('barcode', None),
                map_code=self.request.query_params.get('map_code', None),
                size=self.request.query_params.get('size', None),
                color=self.request.query_params.get('color', None),
                costumer_name=self.request.query_params.get(
                    'costumer_name', None),
            )
            queryset = self.manager.filter_transfers(
                status=status,
                service_provider=service_provider,
                worker=worker,
                carpets=carpet_ids,  # Use filtered carpet IDs here
                services=services,
                start_date=start_date,
                end_date=end_date,
            )
        except Http404 as e:
            # Correct the attribute here
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return queryset
