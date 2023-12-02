from django.urls import path
from .api import *

urlpatterns = [

    path('register/',RegisterUser.as_view(),name=''),
    path('carpet/all-carpets-list/',GetCarpet.as_view(),name='getcarpet'),
    path('carpet/detail/<pk>/',CarpetDetails.as_view(),name='carpetdetail'),
    path('serviceprovider/all-serviceproviders-list/',GetDetailServiceprovider.as_view(),name='getserviceprovider'),
    path('services/all-services-list/',GetServices.as_view(),name='getservices'),
    
    path('carpet/register-from-excel/',CarpetFromExcel.as_view()),
    path('transfer/create-transfer/',PostTransfer.as_view()),
    path('transfer/all-transfer-list/',GetTransfer.as_view()),
    path('transfer/update-transfer/',UpdateTransfer.as_view()),
    
    
    path('updateservice/',UpdateServiceProviders.as_view(),name='updateservice'),
    path('getstatus/',GetStatus.as_view(),name='getsatus'),
    path('updatecarpet/',UpdateCarpet.as_view(),name='updatecarpet'),
    path('getuser/',GetUserDetail.as_view(),name='getuserdetail'),
   # path('getusertoken/',GetUserToken.as_view(),name='getusertoken'),
    
    
    
    

    
]