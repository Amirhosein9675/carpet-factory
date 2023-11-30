from django.urls import path
from .api import *

urlpatterns = [

    path('register/user/',RegisterUser.as_view(),name=''),
    path('get/carpet/',GetCarpet.as_view(),name='getcarpet'),
    path('get/detail/carpet/<pk>/',CarpetDetails.as_view(),name='carpetdetail'),
    path('get/detail/serviceprovider/',GetDetailServiceprovider.as_view(),name='getserviceprovider'),
    path('get/services/',GetServices.as_view(),name='getservices'),
    
    path('registerexcel/',RigisterExcel.as_view(),name='registerexcel'),
    path('updateservice/',UpdateServiceProviders.as_view(),name='updateservice'),
    path('getstatus/',GetStatus.as_view(),name='getsatus'),
    path('updatecarpet/',UpdateCarpet.as_view(),name='updatecarpet'),
    path('getuser/',GetUserDetail.as_view(),name='getuserdetail'),
    path('getusertoken/',GetUserToken.as_view(),name='getusertoken'),
    
    
    
    

    
]