from django.urls import path
from .api import *
from .views import CustomUserDetailsView
urlpatterns = [

    path('register/', RegisterUser.as_view(), name=''),
    path('user/all-user-list/', UserList.as_view()),

    path('carpet/all-carpets-list/', GetCarpet.as_view(), name='getcarpet'),
    path('carpet/detail/<pk>/', CarpetDetails.as_view(), name='carpetdetail'),
    path('carpet/register-from-excel/', CarpetFromExcel.as_view()),
    
    path('transfer/filter-carpet2/', TransferCarpet2.as_view()),


    path('transfer/create-transfer/', PostTransfer.as_view()),
    path('transfer/all-transfer-list/', GetTransfer.as_view()),
    path('transfer/update-transfer/', UpdateTransfer.as_view()),
    path('transfer/update/<int:pk>/', UpdateTransferByDRF.as_view()),
    path('transfer/filter-carpet/', TransferCarpet.as_view()),
    path('transfer/transfer-/', UpdateTransferByDRF.as_view()),
    
    path('transfer/create-transfer2/', TestCreateTransfer.as_view()),
    

    path('status/all-status-list/', GetStatus.as_view()),

    path('user/all-user-list/', UserList.as_view()),

    path('driver/all-driver-list/', DriverList.as_view()),
    path('driver/create-driver/', DriverCreate.as_view()),

    path('serviceprovider/all-serviceproviders-list/',
         ServiceproviderList.as_view(), name='getserviceprovider'),
    path('serviceprovider/create-serviceproviders/',
         ServiceproviderCreate.as_view()),


    path('updateservice/', UpdateServiceProviders.as_view(), name='updateservice'),
    path('updatecarpet/', UpdateCarpet.as_view(), name='updatecarpet'),
    path('getuser/', GetUserDetail.as_view(), name='getuserdetail'),
    # path('getusertoken/',GetUserToken.as_view(),name='getusertoken'),



    path('services/all-services-list/',
         GetServices.as_view(), name='getservices'),
    
    path('api/account/user/', CustomUserDetailsView.as_view(), name='user-details'),



]

   
