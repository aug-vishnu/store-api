from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from auth_api.models import *
from auth_api.serializers import *


#########################################################################
# Start Customer CRUD
#########################################################################
@api_view(['POST','PUT', 'DELETE' ])
def CustomerCUDView(request):
    trail = {}

    # Create Customer
    if request.method == 'POST':
        serializer = CustomerCreateSerializer(data=request.data)
        shop = ShopModel.objects.get(shop_id = request.data.get("shop_id"))

        if serializer.is_valid():
            new_object = serializer.save(shop=shop)
            trail['message'] = "Customer Sucessfully Created"
            trail["data"] =  serializer.data

            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)

    # Edit Customer
    if request.method == 'PUT':
        print(request.data)
        try:
            customer = CustomerModel.objects.filter(shop = request.user.shop).get(customer_id = request.data.get('customer_id'))        
        except:
            raise serializers.ValidationError('Not Found')

        serializer = CustomerEditSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            trail["message"] = "Customer Successfully Updated"
            trail["data"] =  serializer.data
            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)
        
    # Delet Customer
    if request.method == 'DELETE':
        try:
            customer = CustomerModel.objects.filter(shop = request.user.shop).get(customer_id = request.data.get('customer_id'))
        except:
            raise serializers.ValidationError('Not Found')
        customer.delete()
        trail["message"] = "Customer Successfully Deleted"
        return Response(trail, status=status.HTTP_200_OK)
        
#########################################################################


#########################################################################
# Customer List from app
@api_view(['POST', ])
def CustomerListView(request):
    if request.method == 'POST':
        try:
            factors = CustomerModel.objects.filter(shop = request.user.shop)
        except:
            raise serializers.ValidationError('Not Authorized')

        trail = []
        frag = {}
        for i in range(0, len(factors)):
            frag['label'] = str(factors[i].customer_name) + ' : ' + str(factors[i].customer_mobile) 

            frag['customer_id'] = factors[i].customer_id
            frag['customer_mail'] = factors[i].user.username

            frag['customer_mobile'] = factors[i].customer_mobile
            frag['customer_balance'] = factors[i].customer_balance
            frag['customer_type'] = factors[i].customer_type
            frag['customer_address_1'] = factors[i].customer_address_1
            frag['customer_address_2'] = factors[i].customer_address_2
            frag['customer_address_3'] = factors[i].customer_address_3
            frag['customer_name'] = factors[i].customer_name

            trail.append(frag)
            frag = {}
        return Response(trail)
        
#########################################################################


#########################################################################
# Customer Detail from app
@api_view(['POST', ])
def CustomerDetailView(request):
    if request.method == 'POST':
        try:
            factor = CustomerModel.objects.filter(shop = request.user.shop).get(customer_id = request.data.get('customer_id'))
        except:
            raise serializers.ValidationError('Not Authorized')
        frag = {}
        frag['shop_name'] = factor.shop.shop_name
        frag['shop_id'] = factor.shop.shop_id

        frag['customer_id'] = factor.customer_id
        frag['customer_mobile'] = factor.customer_mobile
        frag['customer_balance'] = factor.customer_balance
        frag['customer_type'] = factor.customer_type
        frag['customer_address_1'] = factor.customer_address_1
        frag['customer_address_2'] = factor.customer_address_2
        frag['customer_address_3'] = factor.customer_address_3
        frag['customer_name'] = factor.customer_name
        
        return Response(frag)

#########################################################################
##  End Customer CRUD  ##
#########################################################################