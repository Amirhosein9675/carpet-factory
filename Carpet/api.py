from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from .serializers import *
import json


class RegisterUser(APIView):
    def post(self, request, format=None):
        try:
            seria = RegisterUserSerializer(data=request.data)
            if seria.is_valid():
                username = seria.data.get('username')
                password = seria.data.get('password')
                firstname = seria.data.get('firstname')
                lastname = seria.data.get('lastname')
                p_number = seria.data.get('p_number')
                roole = seria.data.get('roole')
            else:
                return Response({'status': 'bad request serializer not valid'}, status=status.HTTP_400_BAD_REQUEST)
            for valid_user in User.objects.all():
                if valid_user.username == username:
                    return Response({'status': 'username allready exsit'}, status=status.HTTP_400_BAD_REQUEST)
            user1 = User()
            user1.username = username
            user1.password = password
            user1.first_name = firstname
            user1.last_name = lastname
            user1.save()
            if roole == 'admin':
                person = Admin()
                person.user = user1
                person.phone_number = p_number
                person.save()

            elif roole == 'worker':
                person = Worker()
                person.user = user1
                person.phone_number = p_number
                person.save()

            elif roole == 'serviceproviders':
                person = ServiceProviders()
                person.user = user1
                person.phone_number = p_number
                person.save()

            elif roole == 'driver':
                person = Driver()
                person.user = user1
                person.phone_number = p_number
                person.save()

            else:
                return Response({'status': 'The entered key is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': 'okkk'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RigisterExcel(APIView):
    def post(self, request, format=None):
        try:
            import pandas as pd
            import json
            import csv
            import os
            ext = os.path.splitext(str(request.FILES['excel']))[1]
            valid_extentions = ['.xlsx', '.csv']
            if not ext.lower() in valid_extentions:
                return Response({'status': 'The file format is not correct'}, status=status.HTTP_400_BAD_REQUEST)

            # if ext=='.csv':
                # dl=pd.read_csv(request.FILES['excel'])
                # f=dl.to_json(orient='records', indent=4)
                # obj1=json.loads(f)
                # print(obj1)
                # all=[]
                # for raw in obj1:
                # all.append(raw)
                # print(all)

            path_excel = request.FILES['excel']
            df = pd.read_excel(path_excel, engine='openpyxl')
            json_data = df.to_json(orient='records', indent=4)
            obj = json.loads(json_data)

            for obj_dict in obj:
                carp_fac = CarpetFactory()
                carp_fac.title = obj_dict.get('title')
                carp_fac.carpet_id = obj_dict.get('carpet_id')
                carp_fac.save()
            return Response({'status': 'The Excel file was saved in the database'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class GetService_provider(ListAPIView):
    queryset = ServiceProviders.objects.all()
    serializer_class = GetServiceProviderSerializer


class GetCarpet(ListAPIView):
    queryset = Carpet.objects.all()
    serializer_class = GetCarpetSerializer


class GetStatus(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = GetStatusSerializer


class UpdateCarpet(APIView):

    def post(self, request):
        try:
            staus_upadat = Status.objects.get(id=request.data['status_id'])
            print(request.data['status_id'])
            print(staus_upadat)
            carpet = Carpet.objects.filter(
                id=request.data['carpet_id']).update(status=staus_upadat)
            return Response({'status': 'okk'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
