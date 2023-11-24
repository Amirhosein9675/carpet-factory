from django.urls import path
from .api import *

urlpatterns = [

    path('registeruser/',RegisterUser.as_view(),name='register'),
    path('registerexcel/',RigisterExcel.as_view(),name='registerexcel'),
    path('getservice/',GetServices.as_view(),name='getservice'),
    path('getserviceprovider/',GetService_provider.as_view(),name='getserviceprovider'),
    path('updateservice/',UpdateServiceProviders.as_view(),name='updateservice'),
    path('getcarpet/',GetCarpet.as_view(),name='getcarpet'),
    path('getstatus/',GetStatus.as_view(),name='getsatus'),
    path('updatecarpet/',UpdateCarpet.as_view(),name='updatecarpet'),
    
    
    

    
]