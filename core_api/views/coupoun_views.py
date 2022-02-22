from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status


from core_api.serializers import *
from core_api.models import *


#########################################################################
##  Start Apply Coupoun  ##
#########################################################################
@api_view(['POST','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def apply_coupoun(request):
    if request.method == 'POST':
        frag = {'message': 'Coupoun successfully Applied'}
        try:
            coupoun = CoupounModel.objects.filter(shop=request.user.shop).get(coupoun_code = request.data.get('coupoun_code'))
            order = OrderModel.objects.filter(shop=request.user.shop).get(order_id = request.data.get('order_id'))
        except:
            return Response({'error': 'Coupouns/Orders Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)
        print(coupoun, order)
        if coupoun.coupoun_remaining_limit != 0 and not order.coupoun_applied:
            if coupoun.coupoun_min_value <= order.order_price:
                _order_discount_price = (int(order.order_price) * (int(coupoun.coupoun_discount)/100))
                order_discount_price = int(order.order_price) - (_order_discount_price)
                if order_discount_price > coupoun.coupoun_max_discount:
                    order_discount_price = int(order.order_price) - coupoun.coupoun_max_discount
                order.order_discounted_price = order_discount_price
                order.coupoun_applied = True
                coupoun.coupoun_remaining_limit -= 1
                coupoun.save()
                order.save()
            else:
                return Response({'error': 'Coupoun not applicable not met minimum amount to apply'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Run out of coupoun'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(frag, status=status.HTTP_200_OK)

@api_view(['POST','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_coupoun(request):
    if request.method == 'POST':
        frag = {'message': 'Coupoun removed successfully'}
        try:
            coupoun = CoupounModel.objects.filter(shop=request.user.shop).get(coupoun_code = request.data.get('coupoun_code'))
            order = OrderModel.objects.filter(shop=request.user.shop).get(order_id = request.data.get('order_id'))
        except:
            return Response({'error': 'Coupouns/Orders Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        print(coupoun, order)
        order.order_discounted_price = order.order_price
        coupoun.coupoun_remaining_limit += 1
        order.coupoun_applied = False
        coupoun.save()
        order.save()
        
        return Response(frag, status=status.HTTP_200_OK)

#########################################################################
##  End Apply Coupoun  ##
#########################################################################



#########################################################################
##  Start Coupoun CRUD  ##
#########################################################################
# Create Coupoun
@api_view(['POST','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def CoupounCUDView(request):
    if request.method == 'POST':
        print(request.data)
        dupe_products_code = CoupounModel.objects.filter(shop=request.user.shop).filter(coupoun_code = request.data.get('coupoun_code'))
        if(len(dupe_products_code) >= 1 ):
            return Response({'error': 'Coupoun code already exists'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CoupounCreateSerializer(data=request.data)
        frag = {}
        if serializer.is_valid():
            sobject = serializer.save(user=request.user)
            frag['message'] = "Coupoun Sucessfully Registered"
            frag['data'] = serializer.data
        else:
            frag = serializer.errors
        return Response(frag, status=status.HTTP_200_OK)

    
    if request.method == 'PUT':
        try:
            product = CoupounModel.objects.filter(shop=request.user.shop).get(coupoun_id=request.data.get('coupoun_id'))
        except:
            return Response({'error': 'Coupoun Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = EditCoupounSerializer(product, data=request.data)
        frag = {}
        if serializer.is_valid():
            serializer.save()
            frag["message"] = "Coupoun Successfully Updated"
            frag["data"] = serializer.data
            return Response(frag, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        try:
            product = CoupounModel.objects.filter(shop=request.user.shop).get(coupoun_id=request.data.get('coupoun_id'))
        except:
            return Response({'error': 'Coupoun Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        product.delete()
        frag = {}
        frag["message"] = "Coupoun Successfully Deleted"
        return Response(frag, status=status.HTTP_200_OK)


#########################################################################
# Coupoun List from shop
@api_view(['POST', ])
def CoupounListView(request):
    if request.method == 'POST':
        frag = {}
        try:
            factors = CoupounModel.objects.filter(shop=request.user.shop)
        except:
            return Response({'error': 'Coupouns Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)
        trail = []
        for i in range(0, len(factors)):
            frag['coupoun_id'] = factors[i].coupoun_id
            # frag['label'] = str(factors[i].coupoun_code) + ' - ' + str(factors[i].coupoun_name) 

            frag['coupoun_code'] = factors[i].coupoun_code
            frag['coupoun_description'] = factors[i].coupoun_description
            frag['coupoun_min_value'] = factors[i].coupoun_min_value
            frag['coupoun_discount'] = factors[i].coupoun_discount
            frag['coupoun_max_discount'] = factors[i].coupoun_max_discount
            
            frag['coupoun_limit'] = factors[i].coupoun_limit
            frag['coupoun_expiry'] = factors[i].coupoun_expiry
            frag['coupoun_type'] = factors[i].coupoun_type

            frag['time_stamp'] = factors[i].time_stamp

            trail.append(frag)
            frag = {}
        return Response(trail, status=status.HTTP_200_OK)

# #########################################################################
# # Coupoun Detail
# @api_view(['POST', ])
# def CoupounDetailView(request):
#     if request.method == 'POST':
#         frag = {}
#         print(request.data)
#         try:
#             product = CoupounModel.objects.filter(shop=request.user.shop).get(coupoun_id=request.data.get('coupoun_id'))
#         except:
#             return Response({'error': 'Coupoun Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

#         frag['coupoun_id'] = factor.coupoun_id

#         frag['coupoun_code'] = factor.coupoun_code
#         frag['coupoun_name'] = factor.coupoun_name
#         frag['coupoun_gst'] = factor.coupoun_gst
#         frag['coupoun_stock'] = factor.coupoun_stock
        
#         frag['coupoun_vendor_price'] = factor.coupoun_vendor_price
#         frag['coupoun_mrp_price'] = factor.coupoun_mrp_price
        
#         frag['coupoun_available'] = factor.coupoun_available
         
#         return Response(data, status=status.HTTP_200_OK)



# #########################################################################
# ##  End Coupoun CRUD  ##
# #########################################################################




#########################################################################





