from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

from core_api.views.product_views import *
from core_api.views.coupoun_views import *
from core_api.views.basket_views import *
from core_api.views.invoice_views import *



urlpatterns = [
     #################################################
    # Start [ Product - product ] Views frorm product_views.py

    # ProductModel CRUD
    path('product-cud/', ProductCUDView),
    path('product-list/', ProductListView),
    path('product-detail/', ProductDetailView),

    # End Product Views frorm product_views.py
    #################################################


    #################################################
    # Start [ Coupoun - coupoun ] Views frorm coupoun_views.py

    # CoupounModel CRUD
    path('coupoun-cud/', CoupounCUDView),
    path('coupoun-list/', CoupounListView),
    path('coupoun-apply/', apply_coupoun),
    path('coupoun-remove/', remove_coupoun),
    # path('coupoun-detail/', CoupounDetailView),

    # End Coupoun Views frorm coupoun_views.py
    #################################################

     #################################################
    # Start Order - order Views frorm order_views.py
 
    # [ OrderItem - order-item] OrderItemModel CRUD 
    path('order-item-cud/', OrderItemCUDView),

    # [ RandomItem - random-item] RandomItemModel CRUD 
    path('random-item-cud/', RandomItemCUDView),

     # [ Basket - basket] BasketModel CRUD
    path('basket-list/', BasketListView),

     # Checkout View 
    path('check-out/', CheckoutView),

    # [ Sales - sales] SalesModel CRUD 
    path('invoice-detail/', InvoicedetailView),

    # End Order - order Views frorm order_views.py/
    #################################################
     

    #################################################
    # Start Bookings - booking Views frorm booking_views.py

    # [ Sales - sales] SalesModel CRUD 
    path('sales-list/', SalesListView),

    # End Bookings - booking Views frorm booking_views.py
    #################################################


]


