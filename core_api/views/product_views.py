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
##  Start Product CRUD  ##
#########################################################################
# Create Product
@api_view(['POST','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProductCUDView(request):
    if request.method == 'POST':
        print(request.data)
        dupe_products_code = ProductModel.objects.filter(shop=request.user.shop).filter(product_code = request.data.get('product_code'))
        if(len(dupe_products_code) >= 1 ):
            return Response({'error': 'Product code already exists'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductCreateSerializer(data=request.data)
        frag = {}
        if serializer.is_valid():
            sobject = serializer.save(user=request.user)
            frag['message'] = "Product Sucessfully Registered"
            frag['product_name'] = sobject.product_name
        else:
            frag = serializer.errors
        return Response(frag, status=status.HTTP_200_OK)

    
    if request.method == 'PUT':
        try:
            product = ProductModel.objects.filter(shop=request.user.shop).get(product_id=request.data.get('product_id'))
        except:
            return Response({'error': 'Product Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = EditProductSerializer(product, data=request.data)
        frag = {}
        if serializer.is_valid():
            serializer.save()
            frag["message"] = "Product Successfully Updated"
            frag["data"] = serializer.data
            return Response(frag, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        try:
            product = ProductModel.objects.filter(shop=request.user.shop).get(product_id=request.data.get('product_id'))
        except:
            return Response({'error': 'Product Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        product.delete()
        frag = {}
        frag["message"] = "Product Successfully Deleted"
        return Response(frag, status=status.HTTP_200_OK)


#########################################################################
# Product List from shop
@api_view(['POST', ])
def ProductListView(request):
    if request.method == 'POST':
        frag = {}
        try:
            # factors = ProductModel.objects.filter(shop=request.user.shop)
            factors = ProductModel.objects.all()
        except:
            return Response({'error': 'Products Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)
        trail = []
        for i in range(0, len(factors)):
            frag['product_id'] = factors[i].product_id
            frag['label'] = str(factors[i].product_code) + ' - ' + str(factors[i].product_name) 

            frag['product_code'] = factors[i].product_code
            frag['product_name'] = factors[i].product_name
            frag['product_gst'] = factors[i].product_gst
            frag['product_stock'] = factors[i].product_stock
            
            frag['product_vendor_price'] = factors[i].product_vendor_price
            frag['product_mrp_price'] = factors[i].product_mrp_price
            
            frag['product_available'] = factors[i].product_available

            frag['time_stamp'] = factors[i].time_stamp

            trail.append(frag)
            frag = {}
        return Response(trail, status=status.HTTP_200_OK)

#########################################################################
# Product Detail
@api_view(['POST', ])
def ProductDetailView(request):
    if request.method == 'POST':
        frag = {}
        print(request.data)
        try:
            product = ProductModel.objects.filter(shop=request.user.shop).get(product_id=request.data.get('product_id'))
        except:
            return Response({'error': 'Product Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        frag['product_id'] = factor.product_id

        frag['product_code'] = factor.product_code
        frag['product_name'] = factor.product_name
        frag['product_gst'] = factor.product_gst
        frag['product_stock'] = factor.product_stock
        
        frag['product_vendor_price'] = factor.product_vendor_price
        frag['product_mrp_price'] = factor.product_mrp_price
        
        frag['product_available'] = factor.product_available
         
        return Response(data, status=status.HTTP_200_OK)



#########################################################################
##  End Product CRUD  ##
#########################################################################




#########################################################################





