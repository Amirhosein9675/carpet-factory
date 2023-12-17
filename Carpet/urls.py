from django.urls import path
from .api import *
from .views import CustomUserDetailsView
urlpatterns = [
    # register url
    path('register/', RegisterUser.as_view(), name=''),
    # user urls
    path('user/all-user-list/', UserList.as_view()),
    path('getuser/', GetUserDetail.as_view(), name='getuserdetail'),
    path('api/account/user/', CustomUserDetailsView.as_view(), name='user-details'),
    path('user/delete-user/<int:pk>/', DestroyUser.as_view()),
    path('user/update-user/<int:pk>/', UserUpdatePatch.as_view()),

    # sevices urls
    path('services/all-services-list/',
         GetServices.as_view(), name='getservices'),
    path('services/create-services/', ServiceCreate.as_view(), ),
    path('service/delete-service/<int:pk>/', DestroyService.as_view(), ),
    path('service/update-service/<int:pk>/', ServiceUpdatePatch.as_view(), ),
    # carpet urls
    path('carpet/all-carpets-list/', GetCarpet.as_view(), name='getcarpet'),
    path('carpet/detail/<pk>/', CarpetDetails.as_view(), name='carpetdetail'),
    path('carpet/register-from-excel/', CarpetFromExcel.as_view()),
    path('updatecarpet/', UpdateCarpet.as_view(), name='updatecarpet'),
    path('carpet/delete-carpet/<int:pk>/', DestroyCarpet.as_view()),
    path('carpet/update-carpet/<int:pk>/', CarpetUpdatePatch.as_view()),
    path('carpet/size-carpet-list/', CarpetListSize.as_view()),
    path('carpet/kind-carpet-list/', CarpetListKind.as_view()),
    # serviceprovider url
    path('updateservice/', UpdateServiceProviders.as_view(), name='updateservice'),
    path('serviceprovider/all-serviceproviders-list/',
         ServiceproviderList.as_view(), name='getserviceprovider'),
    path('serviceprovider/create-serviceproviders/',
         ServiceproviderCreate.as_view()),
    path('serviceprovider/delete-serviceprovider/<int:pk>/',
         DestroyServiceProvider.as_view()),
    path('serviceprovider/update-serviceprovider/<int:pk>/',
         ServiceProviderUpdatePatch.as_view()),
    # driver urls
    path('driver/all-driver-list/', DriverList.as_view()),
    path('driver/create-driver/', DriverCreate.as_view()),
    path('driver/delete-driver/<int:pk>/', DestroyDriver.as_view()),
    path('driver/update-driver/<int:pk>/', DriverUpdatePatch.as_view()),
    # status url
    path('status/all-status-list/', GetStatus.as_view()),
    path('status/delete-status/<int:pk>/', DestroyStatus.as_view()),
    path('status/update-status/<int:pk>/', StatusUpdatePatch.as_view()),
    # transfer urls
    path('transfer/all-transfer-list/', TransferListAPIView.as_view()),
    path('transfer/update-transfer2/<int:pk>/partial-update/',
         TransferPartialUpdateView.as_view()),
    path('transfer/update-transfer2/<int:pk>/',
         TestTransferUpdateView.as_view()),
    path('transfer/create-transfer2/', TestCreateTransfer.as_view()),
    path('transfer/delete-transfer/<int:pk>/', DestroyTransfer.as_view()),
    path('transfer/admin-verify-transfer/', TransferAdminVerify.as_view()),
    path('transfer/worker-isfinished-transfer/', WorkerTransfer.as_view()),

    # Statistics urls
    path('statistics/all-statistics-list/', StatisticsList.as_view()),
    path('statistics/create-statistics/', StatisticsCreate.as_view()),
    path('statistics/update-statistics/<int:pk>/', StatisticsUpdate.as_view()),

]
