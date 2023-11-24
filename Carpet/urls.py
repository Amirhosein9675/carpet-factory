from django.urls import path
from .api import RegisterUser,RigisterExcel,GetServices,UpdateServiceProviders,GetService_provider

urlpatterns = [

    path('registeruser/',RegisterUser.as_view(),name='register'),
    path('registerexcel/',RigisterExcel.as_view(),name='registerexcel'),
    path('getservice/',GetServices.as_view(),name='getservice'),
    path('getserviceprovider/',GetService_provider.as_view(),name='getserviceprovider'),
    path('updateservice/',UpdateServiceProviders.as_view(),name='updateservice'),
    

    
]