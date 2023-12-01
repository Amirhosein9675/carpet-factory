from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from .serializers import *
import json
from datetime import datetime


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


class GetDetailServiceprovider(ListAPIView):
    queryset = ServiceProviders.objects.all()
    serializer_class = GetServiceProviderSerializer


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
    def post(self, request, format=None):
        try:
            for item in list(request.data.keys()):
                if item not in ['carpets', 'status', 'service_provider', 'services', 'worker', 'date', 'is_finished', 'admin_verify']:
                    return Response({'status': f'key {item} is wrong'}, status=status.HTTP_400_BAD_REQUEST)

        
            worker = User.objects.get(id=request.data['worker'])
            service_provider = ServiceProviders.objects.get(id=request.data['service_provider'])
            date_string_2 = request.data['date']
            format_2 = "%d/%m/%Y %H:%M:%S"
            date_2 = datetime.strptime(date_string_2, format_2)
            trans = Transfer(worker=worker, service_provider=service_provider, date=date_2)
            trans.save()

            list_carpet=request.data['carpets']
            for carpet_item in list_carpet:
                carpet=Carpet.objects.get(barcode=carpet_item)
                trans.carpets.add(carpet)
                
            list_services=request.data['services']
            for services_item in list_services:
                service=Service.objects.get(id=services_item)
                trans.services.add(service)            


            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTransfer(ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = GetTransferSerializers

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


class GetUserToken(ListAPIView):
    def get_queryset(self):
        print(80*'-')
        # print(self.queryset.user)
        # print(self.queryset.auth)
        print(80*'-')
        return User.objects.all()
    serializer_class = GetUserTokenSerializer
