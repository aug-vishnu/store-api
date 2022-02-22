from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from datetime import date
from auth_api.models import *
from auth_api.serializers import *
from auth_api.models import *

#########################################################################
# Start Shop CRUD
#########################################################################
@api_view(['POST','PUT', 'DELETE' ])
def ShopCUDView(request):
    trail = {}

    # Create Factor
    if request.method == 'POST':
        print(request.data)
        serializer = ShopCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_object = serializer.save(user=request.user)
            trail['message'] = "Shop Sucessfully Created"
            trail['shop_id'] = new_object.shop_id
            trail['shop_name'] = new_object.shop_name
            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)


    # Edit Factor
    if request.method == 'PUT':
        try:
            shop = ShopModel.objects.get(shop_id=request.data.get("shop_id"))
        except:
            raise serializers.ValidationError('Not Found')

        serializer = ShopEditSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            trail["message"] = "Shop Successfully Updated"
            trail["data"] =  serializer.data
            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)

    # Delet Factor
    if request.method == 'DELETE':
        try:
            shop = ShopModel.objects.get(shop_id=request.data.get("shop_id"))
        except:
            raise serializers.ValidationError('Not Found')
        shop.delete()
        trail["message"] = "Shop Successfully Deleted"
        return Response(trail, status=status.HTTP_200_OK)

#########################################################################


#########################################################################
# Shop List from app
@api_view(['POST', ])
def ShopListView(request):
    if request.method == 'POST':
        factors = ShopModel.objects.all()
        trail = []
        frag = {}
        for i in range(0, len(factors)):
            frag['shop_name'] = factors[i].shop_name
            frag['shop_id'] = factors[i].shop_id
            frag['shop_address'] = factors[i].shop_address
            frag['shop_mobile'] = factors[i].shop_mobile
            frag['shop_license'] = factors[i].shop_license
            frag['subscription_type'] = factors[i].subscription_type
            frag['subscription_start'] = factors[i].subscription_start
            frag['subscription_end'] = factors[i].subscription_end
            trail.append(frag)
            frag = {}
        return Response(trail)

#########################################################################


#########################################################################
# Shop Detail from app
@api_view(['POST', ])
def ShopDetailView(request):
    if request.method == 'POST':
        # print(request.user.shop)

        factor = ShopModel.objects.get(shop_id = request.data.get("shop_id"))
        # factor = ShopModel.objects.get(shop_id = request.user.shop.shop_id)

        # try:
        # except:
        #     raise serializers.ValidationError('Not Found')

        frag = {}
        frag['shop_name'] = factor.shop_name
        frag['shop_id'] = factor.shop_id
        frag['shop_active'] = factor.shop_active
        frag['shop_address'] = factor.shop_address
        frag['shop_mobile'] = factor.shop_mobile
        frag['shop_logo'] = factor.shop_logo
        frag['subscription_type'] = factor.subscription_type
        frag['subscription_start'] = factor.subscription_start
        frag['subscription_end'] = factor.subscription_end

        # ##################################################################################
        # today = date.today()
        # product_valuation = 0
        # month_revenue = 0
        # day_revenue = 0

        # products = ProductModel.objects.filter(shop = factor)
        # orders = OrderModel.objects.filter(shop = factor).filter(time_stamp__month = today.month)

        # for x in range(0, len(products)):
        #     if (products[x].product_stock):
        #         product_valuation += products[x].product_stock * products[x].product_mrp_price

        # for x in range(0, len(orders)):
        #     month_revenue += orders[x].order_price

        # frag['product_count'] = len(products)
        # frag['product_valuation'] = product_valuation
        # frag['month_revenue'] = month_revenue

        # orders = orders.filter(time_stamp__day = today.day)
        # for x in range(0, len(orders)):
        #     day_revenue += orders[x].order_price
        # frag['day_revenue'] = day_revenue

        # print(orders)
        # ##################################################################################

        # # User Details { Admin, Subadmin }
        # user = request.user
        # if user.user_type == 1:
        #     frag['username'] = user.username
        #     frag['mobile_number'] = user.mobile_number
        #     frag['user_type'] = user.user_type
        #     owner = AdminModel.objects.get(user = user)
        #     frag['owner_name'] = owner.owner_name
        #     frag['owner_address'] = owner.owner_address
        #     frag['owner_mobile'] = owner.owner_mobile

        #     frag['user_database'] = 1
        #     frag['lead_followup'] = 1
        #     frag['invoice_followup'] = 1
        #     frag['task_followup'] = 1
        #     frag['journal'] = 1


        # elif user.user_type == 2:
        #     frag['username'] = user.username
        #     frag['mobile_number'] = user.mobile_number
        #     frag['user_type'] = user.user_type

        #     manager = SubadminModel.objects.get(user = user)
        #     print(user.shop)
        #     manager_permission = SubadminPermisionModel.objects.get(shop = user.shop)

        #     frag['manager_name'] = manager.manager_name
        #     frag['manager_address'] = manager.manager_address
        #     frag['manager_mobile'] = manager.manager_mobile

        #     frag['user_database'] = manager_permission.user_database
        #     frag['lead_followup'] = manager_permission.lead_followup
        #     frag['invoice_followup'] = manager_permission.invoice_followup
        #     frag['task_followup'] = manager_permission.task_followup
        #     frag['journal'] = manager_permission.journal



        return Response(frag)

#########################################################################
##  End Shop CRUD  ##
#########################################################################





#########################################################################
#  Party Update Delete
@api_view(['POST',])
def BankDetailsUpdateView(request):
    admin = Admin.objects.get(user=request.user.user_id)
    shop = Shop.objects.get(shop_license=admin.shop)
    bankdetail = Bankdetails.objects.filter(shop=shop)

    if request.method == 'POST':
        serializer = EditPartySerializer(bankdetail[0], data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["message"] = "Successfully Updated"
            data["Data"] = serializer.data

            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


#########################################################################
# Bankdetails Edit bot reqs
@api_view(['POST'])
def BankDetailsUpdateView(request):
    try:
        admin = Admin.objects.get(user=request.user.user_id)
        shop = Shop.objects.get(shop_license=admin.shop)
        bank = Bankdetails.objects.filter(shop=shop)

    except:
        return Response({'message':'Not valid parameters'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        print(request.data)
        serializer = EditBankDetailsSerializer(bank[0], data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["message"] = "Successfully Updated"
            data["Data"] = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors)



#########################################################################
# Start SubadminPermission CRUD
#########################################################################
@api_view(['PUT' ])
def SubadminPermissionCUDView(request):
    trail = {}
    # Edit Factor
    if request.method == 'PUT':
        try:
            manager_permission = SubadminPermisionModel.objects.get(manager_permission_id=request.data.get("manager_permission_id"))
        except:
            raise serializers.ValidationError('Not Found')

        serializer = SubadminPermissionEditSerializer(manager_permission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            trail["message"] = "Subadmin Permission Successfully Updated"
            trail["data"] =  serializer.data
            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)


#########################################################################



#########################################################################
##  End SubadminPermission CRUD  ##
#########################################################################

