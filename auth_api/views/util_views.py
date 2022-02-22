from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from datetime import date
from django.utils import timezone
from core_api.models import *
from core_api.serializers import *

# from core_api.send_mail import send_mail



#########################################################################
##  Start WhoAmI  ##
#########################################################################
# Whoami for basic
@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def WhoAmIView(request):
    if request.method == 'GET':
        data = {}
        account = Account.objects.get(pk=request.user.user_id)
        data['username'] = account.username
        data['email'] = account.email
        data['mobile_number'] = account.mobile_number
        data['user_id'] = account.user_id
        data['user_type'] = account.user_type

        shop = Shop.objects.get(shop_license=request.user.shop)
        data['shop_name'] = shop.shop_name
        data['shop_address_1'] = shop.shop_address
        data['shop_address_2'] = shop.shop_address_2
        data['shop_address_3'] = shop.shop_address_3
        data['invoice_prefix'] = shop.invoice_prefix
        data['gsit'] = shop.gsit
        data['shop_logo'] = shop.shop_logo.url

        try:
            # Bank details
            bank = Bankdetails.objects.filter(shop=shop)
            data['bank_name'] = bank[0].bank_name
            data['bank_account_no'] = bank[0].bank_account_no
            data['bank_branch'] = bank[0].bank_branch
            data['bank_ifsc'] = bank[0].bank_ifsc
            data['upi_id'] = bank[0].UPI_id
        except:
            return Response(data)

        return Response(data)


@api_view(['POST'])
def FirstPingView(request):
    if request.method == 'POST':
        # Variables
        data = {}
        valuation = monthly_revenue = monthly_profit = weekly_revenue = weekly_profit = 0

        #########################################################################
        # Basic data
        shop = Shop.objects.get(shop_license=request.user.shop)
        data['shop_license'] = shop.shop_license
        data['shop_name'] = shop.shop_name
        data['shop_logo'] = shop.shop_logo.url

        account = Account.objects.get(pk=request.user.user_id)
        data['username'] = account.username
        data['mobile_number'] = account.mobile_number

        products = Products.objects.filter(shop=request.user.shop)
        data['no_products'] = len(products)
        for i in range(0, len(products)):
            valuation += (products[i].product_buy_price *
                          products[i].product_stock)
        data['valuation'] = valuation
        #########################################################################

        #########################################################################
        # Initial Analytics
        current = datetime.now(tz=timezone.utc)
        past = current - timedelta(days=7)
        monthly_orders = Order.objects.filter(time_stamp__month=current.month)
        for i in range(0, len(monthly_orders)):
            monthly_revenue += monthly_orders[i].order_price
            for j in range(0, len(monthly_orders[i].order_items.all())):
                current_pd = monthly_orders[i].order_items.all()[j].product
                monthly_profit += (current_pd.product_mrp_price -
                                   current_pd.product_buy_price) * monthly_orders[i].order_items.all()[j].quantity
        data['monthly_profit'] = monthly_profit
        data['monthly_revenue'] = monthly_revenue

        weekly_orders = Order.objects.filter(time_stamp__range=[past, current])
        for i in range(0, len(weekly_orders)):
            weekly_revenue += weekly_orders[i].order_price
            for j in range(0, len(weekly_orders[i].order_items.all())):
                current_pd = weekly_orders[i].order_items.all()[j].product
                weekly_profit += (
                    current_pd.product_mrp_price - current_pd.product_buy_price
                ) * weekly_orders[i].order_items.all()[j].quantity
        data['weekly_profit'] = weekly_profit
        data['weekly_revenue'] = weekly_revenue
        #########################################################################

        return Response(data)


@api_view(['POST'])
def check_username(request):
    if request.method == 'POST':
        isExist = False
        account = Account.objects.filter(
            shop=request.user.shop).all()
        data = request.data.get('data').lower()
        print(data)
        for i in range(0, len(account)):
            if str(data) == account[i].username:
                isExist = True
            if str(data) == account[i].email:
                isExist = True
        if isExist:
            message = {'message': "taken"}
        else:
            message = {'message': "available"}

        return Response(message)


#########################################################################
##  End WhoAmI  ##
#########################################################################

#########################################################################