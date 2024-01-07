from django.db.models import Q,F, Subquery, OuterRef
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from .serializers import *
import json
from django.http import Http404
from rest_framework import pagination
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet


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
                if item not in ['factory', 'barcode', 'map_code', 'size', 'color', 'costumer_name', 'kind', 'density']:
                    return Response({'status': f'key {item} is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            seria = CarpetDetailSerializer(data=request.data)
            if seria.is_valid():
                factory = seria.data.get('factory')
                barcode = seria.data.get('barcode')
                map_code = seria.data.get('map_code')
                size = seria.data.get('size')
                color = seria.data.get('color')
                costumer_name = seria.data.get('costumer_name')
                kind = seria.data.get('kind')
                density = seria.data.get('density')
            else:
                return Response({'status': 'bad request serializer not valid'}, status=status.HTTP_400_BAD_REQUEST)
            carpet_new = Carpet()
            carpet_new.factory = factory
            carpet_new.barcode = barcode
            carpet_new.map_code = map_code
            carpet_new.size = size
            carpet_new.color = color
            carpet_new.costumer_name = costumer_name
            carpet_new.kind = kind
            carpet_new.density = density
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
            if len(request.data['services']) > 0:
                # if len(json.loads(request.data['services'])) > 0:
                list_services = request.data['services']
                # list_services = json.loads(request.data['services'])
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
    serializer_class = DriverListSerializer1


class DriverCreate(CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverListSerializer


class GetStatus(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = GetStatusSerializer


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
                raise e

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

        return Transfer.objects.filter(**filters).distinct()

    def filter_carpet_ids(self, **carpet_filters):
        list_element = list(carpet_filters.values())
        are_all_none = all(element is None for element in list_element)
        if are_all_none:
            return None
        carpet_ids = Carpet.objects.values_list('id', flat=True)
        carpet_fields = [field.name for field in Carpet._meta.get_fields(
        ) if isinstance(field, models.CharField)]
        for field in carpet_fields:
            value = carpet_filters.get(field, None)
            if value is not None:
                carpet_ids = Carpet.objects.filter(
                    **{field: value, 'id__in': carpet_ids}).values_list('id', flat=True)

        if not carpet_ids:
            raise Http404("No matching carpet records found.")
        carpet_ids = list(carpet_ids)
        return carpet_ids


class TransferListAPIView(ListAPIView):
    serializer_class = TransferSerializer1
    queryset = Transfer.objects.all()
    pagination_class = CustomPagination
    manager = TransferManager()

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        service_provider = self.request.query_params.get(
            'service_provider', None)
        worker = self.request.query_params.get('worker', None)
        services = self.request.query_params.get('services', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if end_date and len(end_date) == 10:
            end_date += "T23:59:59"

        try:
            carpet_ids = self.manager.filter_carpet_ids(
                factory=self.request.query_params.get('factory', None),
                barcode=self.request.query_params.get('barcode', None),
                map_code=self.request.query_params.get('map_code', None),
                size=self.request.query_params.get('size', None),
                color=self.request.query_params.get('color', None),
                costumer_name=self.request.query_params.get(
                    'costumer_name', None),
                kind=self.request.query_params.get('kind', None),
                density=self.request.query_params.get('density', None),
            )
            queryset = self.manager.filter_transfers(
                status=status,
                service_provider=service_provider,
                worker=worker,
                carpets=carpet_ids,
                services=services,
                start_date=start_date,
                end_date=end_date,
            )
        except Http404 as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return queryset


class DestroyTransfer(DestroyAPIView):
    queryset = Transfer.objects.all()
    serializer_class = DestroyTransferSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DestroyCarpet(DestroyAPIView):
    queryset = Carpet.objects.all()
    serializer_class = DestroyCarpetSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DestroyDriver(DestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DestroyDriverSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DestroyServiceProvider(DestroyAPIView):
    queryset = ServiceProviders.objects.all()
    serializer_class = DestroyServiceProvidersSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DestroyService(DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = DestroyServiceSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DestroyStatus(DestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = DestroyStatusSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DestroyUser(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = DestroyUserSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransferAdminVerify(ListAPIView):
    serializer_class = AdminVerifyTransferSerializer
    queryset = Transfer.objects.filter(admin_verify=False)


class WorkerTransfer(ListAPIView):
    serializer_class = WorkerTransferSerializer

    def get_queryset(self):

        user = self.request.user
        queryset = Transfer.objects.filter(worker=user, is_finished=False)
        return queryset


class UserUpdatePatch(APIView):
    serializer_class = UserUpdatePatchSerializer

    def patch(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        # if request.user != user:
        #     return Response({"detail": "You do not have permission to update this user"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class StatusUpdatePatch(APIView):
    serializer_class = StatusUpdatePatchSerializer

    def patch(self, request, pk, *args, **kwargs):
        try:
            status_obj = Status.objects.get(pk=pk)
        except Status.DoesNotExist:
            return Response({"detail": "Status not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            status_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceUpdatePatch(APIView):
    serializer_class = ServiceUpdatePatchSerializer

    def patch(self, request, pk, *args, **kwargs):
        try:
            service_obj = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({"detail": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            service_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceProviderUpdatePatch(APIView):
    serializer_class = ServiceProviderUpdatePatchSerializer

    def patch(self, request, pk, *args, **kwargs):
        try:
            service_provider_obj = ServiceProviders.objects.get(pk=pk)
        except ServiceProviders.DoesNotExist:
            return Response({"detail": "Service Provider not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            service_provider_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverUpdatePatch(APIView):
    serializer_class = DriverUpdatePatchSerializer

    def patch(self, request, pk, *args, **kwargs):
        try:
            driver_obj = Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:
            return Response({"detail": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            driver_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarpetUpdatePatch(APIView):
    serializer_class = CarpetUpdatePatchSerializer

    def patch(self, request, pk, *args, **kwargs):
        try:
            carpet_obj = Carpet.objects.get(pk=pk)
        except Carpet.DoesNotExist:
            return Response({"detail": "Carpet not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            carpet_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatisticsList(ListAPIView):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsListSerializer


class StatisticsCreate(CreateAPIView):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsCreateSerializer


class StatisticsUpdate(APIView):
    serializer_class = StatisticsUpdateSerializer

    def patch(self, request, pk, *args, **kwargs):
        try:
            statistics_obj = Statistics.objects.get(pk=pk)
        except Statistics.DoesNotExist:
            return Response({"detail": "Statistics record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            statistics_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarpetListSize(APIView):
    def get(self, request, *args, **kwargs):
        sizes = list(Carpet.objects.values_list('size', flat=True).distinct())
        return Response(sizes)


class CarpetListKind(APIView):
    def get(self, request, *args, **kwargs):
        kinds = list(Carpet.objects.values_list('kind', flat=True).distinct())
        return Response(kinds)


class CarpetListWithTransfersAPIView(ListAPIView):
    serializer_class = CarpetwithTransferSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        carpet_filters = {
            'factory': self.request.query_params.get('factory'),
            'barcode': self.request.query_params.get('barcode'),
            'map_code': self.request.query_params.get('map_code'),
            'size': self.request.query_params.get('size'),
            'color': self.request.query_params.get('color'),
            'costumer_name': self.request.query_params.get('costumer_name'),
            'kind': self.request.query_params.get('kind'),
            'density': self.request.query_params.get('density'),
        }

        transfer_filters = {
            'status': self.request.query_params.get('status'),
            'service_provider': self.request.query_params.get('service_provider'),
            'worker': self.request.query_params.get('worker'),
            'date': self.request.query_params.get('date'),
            'is_finished': self.request.query_params.get('is_finished'),
            'admin_verify': self.request.query_params.get('admin_verify'),
        }

        queryset = Carpet.objects.all()

        for field, value in carpet_filters.items():
            if value:
                queryset = queryset.filter(**{field: value})

        if any(transfer_filters.values()):
            transfer_query = Q()
            transfer_field_mapping = {
                'status': 'status',
                'service_provider': 'service_provider',
                'worker': 'worker',
                'is_finished': 'is_finished',
                'admin_verify': 'admin_verify',
                'date': 'date',
            }

            for field, value in transfer_filters.items():
                if value is not None and field in transfer_field_mapping:
                    if field == 'date':
                        date_start = self.request.query_params.get(
                            'start_date')
                        date_end = self.request.query_params.get('end_date')

                        if date_start and date_end:
                            date_start = timezone.datetime.strptime(
                                date_start, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                            date_end = timezone.datetime.strptime(
                                date_end, '%Y-%m-%d').replace(tzinfo=timezone.utc)
                            transfer_query |= Q(
                                **{'transfers__{}__range'.format(transfer_field_mapping[field]): (date_start, date_end)})
                    else:
                        transfer_query |= Q(
                            **{'transfers__{}'.format(transfer_field_mapping[field]): value})

            queryset = queryset.filter(transfer_query).distinct()

        return queryset


class LastTransferForCarpet(APIView):
    def get(self, request, pk):

        carpet = get_object_or_404(Carpet, id=pk)

        last_transfer = Transfer.objects.filter(
            carpets=carpet).order_by('-date').first()

        if last_transfer:
            serializer = LastTransferSerializer(last_transfer)
            return Response(serializer.data)
        else:
            return Response({"message": "No transfers found for the given carpet ID."}, status=404)


class CarpetTransferFinal(ModelViewSet):
     serializer_class = CarpetTransferFinalFilter
     pagination_class = CustomPagination
     
     def get_queryset(self):
        queryset = Carpet.objects.exclude(transfers=None).exclude(transfers__isnull=True).distinct()
        
    
        factory_filter = self.request.query_params.get('factory', None)
        barcode_filter = self.request.query_params.get('barcode', None)
        size_filter = self.request.query_params.get('size', None)
        map_code_filter = self.request.query_params.get('map_code', None)
        color_filter = self.request.query_params.get('color', None)
        costumer_name_filter = self.request.query_params.get(
            'costumer_name', None)
        kind_filter = self.request.query_params.get('kind', None)
        density_filter = self.request.query_params.get('density', None)

        if factory_filter:
            queryset = queryset.filter(factory=factory_filter)
        if barcode_filter:
            queryset = queryset.filter(barcode=barcode_filter)
        if size_filter:
            queryset = queryset.filter(size=size_filter)
        if map_code_filter:
            queryset = queryset.filter(map_code=map_code_filter)
        if color_filter:
            queryset = queryset.filter(color=color_filter)
        if costumer_name_filter:
            queryset = queryset.filter(costumer_name=costumer_name_filter)
        if kind_filter:
            queryset = queryset.filter(kind=kind_filter)
        if density_filter:
            queryset = queryset.filter(density=density_filter)
        
        status_filter = self.request.query_params.get('status')
        service_provider_filter = self.request.query_params.get('service_provider')
        services_filter = self.request.query_params.get('services')
        worker_filter = self.request.query_params.get('worker')
        date_filter = self.request.query_params.get('date')
        is_finished_filter = self.request.query_params.get('is_finished')
        admin_verify_filter = self.request.query_params.get('admin_verify')
        
        if status_filter:
            queryset = queryset.filter(transfers__status=status_filter)
        if service_provider_filter:
            queryset = queryset.filter(transfers__service_provider=service_provider_filter)
        if services_filter:
            queryset = queryset.filter(transfers__services=services_filter)
        if worker_filter:
            queryset = queryset.filter(transfers__worker=worker_filter)
        if is_finished_filter:
            queryset = queryset.filter(transfers__is_finished=is_finished_filter)
        if admin_verify_filter:
            queryset = queryset.filter(transfers__admin_verify=admin_verify_filter)
            
        date__gte = self.request.query_params.get('date__gte')
        date__lte = self.request.query_params.get('date__lte')
        if date__gte and date__lte:
        
            date__gte = datetime.strptime(date__gte, '%Y-%m-%d')
            date__lte = datetime.strptime(date__lte, '%Y-%m-%d')
            
            queryset = queryset.filter(
                transfers__date__gte=date__gte,
                transfers__date__lte=date__lte
            )
        queryset = queryset.exclude(transfers=None).exclude(transfers__isnull=True)

        return queryset
    
    


class CarpetLastTransferExiteService(ModelViewSet):
    serializer_class = CarpetwithTransferForExitServiceSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        
        last_exit_transfer_subquery = Transfer.objects.filter(
            carpets=OuterRef('id'), status__title='خروج به سرویس'
        ).order_by('-date').values('id')[:1]

        
        queryset = Carpet.objects.annotate(
            last_exit_transfer_id=Subquery(last_exit_transfer_subquery)
        ).filter(last_exit_transfer_id__isnull=False).distinct()

        
        factory_filter = self.request.query_params.get('factory', None)
        barcode_filter = self.request.query_params.get('barcode', None)
        size_filter = self.request.query_params.get('size', None)
        map_code_filter = self.request.query_params.get('map_code', None)
        color_filter = self.request.query_params.get('color', None)
        costumer_name_filter = self.request.query_params.get(
            'costumer_name', None)
        kind_filter = self.request.query_params.get('kind', None)
        density_filter = self.request.query_params.get('density', None)

        if factory_filter:
            queryset = queryset.filter(factory=factory_filter)
        if barcode_filter:
            queryset = queryset.filter(barcode=barcode_filter)
        if size_filter:
            queryset = queryset.filter(size=size_filter)
        if map_code_filter:
            queryset = queryset.filter(map_code=map_code_filter)
        if color_filter:
            queryset = queryset.filter(color=color_filter)
        if costumer_name_filter:
            queryset = queryset.filter(costumer_name=costumer_name_filter)
        if kind_filter:
            queryset = queryset.filter(kind=kind_filter)
        if density_filter:
            queryset = queryset.filter(density=density_filter)

        
        transfer_service_provider_filter = self.request.query_params.get(
            'service_provider', None)
        transfer_worker_filter = self.request.query_params.get('worker', None)
        transfer_services_filter = self.request.query_params.get(
            'services', None)
        transfer_date_gte_filter = self.request.query_params.get(
            'date__gte', None)
        transfer_date_lte_filter = self.request.query_params.get(
            'date__lte', None)
        transfer_is_finished_filter = self.request.query_params.get(
            'is_finished', None)
        transfer_admin_verify_filter = self.request.query_params.get(
            'admin_verify', None)

        if transfer_service_provider_filter:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__service_provider__id=transfer_service_provider_filter)
        if transfer_worker_filter:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__worker__id=transfer_worker_filter)
        if transfer_services_filter:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__services__id=transfer_services_filter)

        if transfer_is_finished_filter is not None:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__admin_verify=bool(transfer_admin_verify_filter))

        if transfer_admin_verify_filter is not None:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__admin_verify=bool(transfer_admin_verify_filter))

        if transfer_date_gte_filter or transfer_date_lte_filter:
            last_exit_transfer_date_subquery = Transfer.objects.filter(
                carpets=OuterRef('id'), status__title='خروج به سرویس'
            ).order_by('-date').values('date')[:1]
            queryset = queryset.annotate(
                last_exit_transfer_date=Subquery(last_exit_transfer_date_subquery))
            if transfer_date_gte_filter:
                queryset = queryset.filter(Q(transfers__date__gte=transfer_date_gte_filter) | Q(
                    last_exit_transfer_date__gte=transfer_date_gte_filter))
            if transfer_date_lte_filter:
                queryset = queryset.filter(Q(transfers__date__lte=transfer_date_lte_filter) | Q(
                    last_exit_transfer_date__lte=transfer_date_lte_filter))
        return queryset
    def get_serializer(self, *args, **kwargs):
        exclude_transfers = self.request.query_params.get('exclude_transfers', None)
        kwargs['context'] = {'exclude_transfers': exclude_transfers == 'true'}
        return super().get_serializer(*args, **kwargs)
    
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if 'results' in response.data:
            for item in response.data['results']:
                if 'transfers' in item and item['transfers'] is not None:
                    del item['transfers']
        return response

class CarpetLastTransferEnterFactory(ModelViewSet):
    serializer_class = CarpetwithTransferForEnterFactorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        
        last_exit_transfer_subquery = Transfer.objects.filter(
            carpets=OuterRef('id'), status__title='ورود از کارخانه'
        ).order_by('-date').values('id')[:1]

        
        queryset = Carpet.objects.annotate(
            last_exit_transfer_id=Subquery(last_exit_transfer_subquery)
        ).filter(last_exit_transfer_id__isnull=False).distinct()

        
        factory_filter = self.request.query_params.get('factory', None)
        barcode_filter = self.request.query_params.get('barcode', None)
        size_filter = self.request.query_params.get('size', None)
        map_code_filter = self.request.query_params.get('map_code', None)
        color_filter = self.request.query_params.get('color', None)
        costumer_name_filter = self.request.query_params.get(
            'costumer_name', None)
        kind_filter = self.request.query_params.get('kind', None)
        density_filter = self.request.query_params.get('density', None)

        if factory_filter:
            queryset = queryset.filter(factory=factory_filter)
        if barcode_filter:
            queryset = queryset.filter(barcode=barcode_filter)
        if size_filter:
            queryset = queryset.filter(size=size_filter)
        if map_code_filter:
            queryset = queryset.filter(map_code=map_code_filter)
        if color_filter:
            queryset = queryset.filter(color=color_filter)
        if costumer_name_filter:
            queryset = queryset.filter(costumer_name=costumer_name_filter)
        if kind_filter:
            queryset = queryset.filter(kind=kind_filter)
        if density_filter:
            queryset = queryset.filter(density=density_filter)

        
        transfer_service_provider_filter = self.request.query_params.get(
            'service_provider', None)
        transfer_worker_filter = self.request.query_params.get('worker', None)
        transfer_services_filter = self.request.query_params.get(
            'services', None)
        transfer_date_gte_filter = self.request.query_params.get(
            'date__gte', None)
        transfer_date_lte_filter = self.request.query_params.get(
            'date__lte', None)
        transfer_is_finished_filter = self.request.query_params.get(
            'is_finished', None)
        transfer_admin_verify_filter = self.request.query_params.get(
            'admin_verify', None)

        if transfer_service_provider_filter:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__service_provider__id=transfer_service_provider_filter)
        if transfer_worker_filter:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__worker__id=transfer_worker_filter)
        if transfer_services_filter:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__services__id=transfer_services_filter)

        if transfer_is_finished_filter is not None:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__admin_verify=bool(transfer_admin_verify_filter))

        if transfer_admin_verify_filter is not None:
            queryset = queryset.filter(transfers__id=F(
                'last_exit_transfer_id'), transfers__admin_verify=bool(transfer_admin_verify_filter))

        if transfer_date_gte_filter or transfer_date_lte_filter:
            last_exit_transfer_date_subquery = Transfer.objects.filter(
                carpets=OuterRef('id'), status__title='ورود از کارخانه'
            ).order_by('-date').values('date')[:1]
            queryset = queryset.annotate(
                last_exit_transfer_date=Subquery(last_exit_transfer_date_subquery))
            if transfer_date_gte_filter:
                queryset = queryset.filter(Q(transfers__date__gte=transfer_date_gte_filter) | Q(
                    last_exit_transfer_date__gte=transfer_date_gte_filter))
            if transfer_date_lte_filter:
                queryset = queryset.filter(Q(transfers__date__lte=transfer_date_lte_filter) | Q(
                    last_exit_transfer_date__lte=transfer_date_lte_filter))
        return queryset
    def get_serializer(self, *args, **kwargs):
        exclude_transfers = self.request.query_params.get('exclude_transfers', None)
        kwargs['context'] = {'exclude_transfers': exclude_transfers == 'true'}
        return super().get_serializer(*args, **kwargs)
    
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if 'results' in response.data:
            for item in response.data['results']:
                if 'transfers' in item and item['transfers'] is not None:
                    del item['transfers']
        return response
