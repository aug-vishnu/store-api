from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

from auth_api.views.shop_views import *
from auth_api.views.user_views import *
from auth_api.views.customer_views import *

urlpatterns = [

    #################################################
    # Start [ Shop - shop ] Views frorm shop_views.py

    # ShopModel CRUD
    path('shop-cud/', ShopCUDView),
    path('shop-list/', ShopListView),
    path('shop-detail/', ShopDetailView),

    # End Shop Views frorm shop_views.py
    #################################################


    #################################################
    # Start [ User - user ] Views frorm user_views.py

    # [ Admin - admin] AdminModel CRUD 
    path('admin-cud/', AdminCUDView),
    path('admin-list/', AdminListView),
    path('admin-detail/', AdminDetailView),

    # [ SubAdmin - sub-admin] SubAdminModel CRUD
    path('sub-admin-cud/', SubAdminCUDView),
    path('sub-admin-list/', SubAdminListView),
    path('sub-admin-detail/', SubAdminDetailView),
    
    path('sub-admin-permission-cud/', SubadminPermissionCUDView),

    # End SubAdmin Views frorm user_views.py
    #################################################


    #################################################
    # Start Customer Views from customer_views.py

    # [ Customer - customer] CustomerModel CRUD
    path('customer-cud/', CustomerCUDView),
    path('customer-list/', CustomerListView),
    path('customer-detail/', CustomerDetailView),

    # End Customer Views frorm customer_views.py
    #################################################


    #################################################
    # Start Distributor Views from customer_views.py

    # [ Distributor - disribitor] DistributorModel CRUD
    path('disribitor-cud/', DistributorCUDView),
    path('disribitor-list/', DistributorListView),
    path('disribitor-detail/', DistributorDetailView),

    # End Distributor Views frorm disribitor_views.py
    #################################################

    
    #################################################
    # Start of Misc
    
    path('login/', obtain_auth_token),
    
    # End of Misc
    #################################################








    # path('userverification/', UserVerificationView),
    # path('resetpassword/', ResetPasswordView),

    # path('forgotpassword/', ForgotPasswordView),
    # path('forgotpasswordchange/', ForgotChangePasswordView),

    # path('checkusername/', CheckUsername),
    
]