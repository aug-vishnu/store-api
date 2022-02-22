from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from core_api.models import *
from core_api.serializers import *


#########################################################################
##  Start OrderItem Features  ##
#########################################################################
# Place your item on Basket
@api_view(['POST','PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def OrderItemCUDView(request):
    if request.method == 'POST':
        serializer = OrderItemCreateSerializer(data=request.data)
        frag = {}
        if serializer.is_valid():
            response = serializer.save(user=request.user)
            frag['response'] = "Order Item added on Basket"
            frag['message'] = serializer.data
        else:
            frag = serializer.errors
        return Response(frag, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        frag = {}
        try:
             orderitem = OrderItemModel.objects.filter(shop=request.user.shop).get(orderitem_id=request.data.get('order_item_id'))
        except:
            return Response({'error': 'Order Item Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)
        quantity = request.data.get('item_quantity')
        product = orderitem.product
        price_with_gst = (product.product_mrp_price + (product.product_mrp_price * (product.product_gst/100))) * int(quantity)
        orderitem.item_quantity = quantity
        orderitem.item_price = price_with_gst
        orderitem.save()

        frag["message"] = "Order Item Successfully Updated"
        frag["order_item_price"] = orderitem.item_price
        frag["order_item_gst_price"] = orderitem.item_gst_price
        frag["order_item_quantity"] = orderitem.item_quantity
        return Response(frag, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        try:
             orderitem = OrderItemModel.objects.filter(shop=request.user.shop).get(orderitem_id=request.data.get('order_item_id'))
        except:
            return Response({'error': 'Order Item Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        orderitem.delete()
        frag = {}
        frag["message"] = "Order Item Successfully Deleted"
        return Response(frag, status=status.HTTP_200_OK)

#########################################################################
##  End OrderItem Features  ##
#########################################################################



#########################################################################



#########################################################################
##  Start RandomItem Features  ##
#########################################################################
# Place your item on Basket
@api_view(['POST','PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def RandomItemCUDView(request):
    frag = {}
    if request.method == 'POST':
        serializer = RandomItemCreateSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save(user=request.user)
            frag['response'] = "Random Item added on Basket"
            frag['message'] = serializer.data
        else:
            frag = serializer.errors
        return Response(frag, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        try:
             randomitem = RandomItemModel.objects.filter(shop=request.user.shop).get(randomitem_id=request.data.get('orderitem_id'))
        except:
            return Response({'error': 'Random Item Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        randomitem.product_gst = request.data.get('product_gst')
        randomitem.product_price = request.data.get('product_price')
        randomitem.product_name = request.data.get('product_name')
        randomitem.product_quantity = request.data.get('product_quantity')

        print(type(randomitem.product_price))
        price_with_gst = (int(randomitem.product_price) + (int(randomitem.product_price) * (int(randomitem.product_gst)/100))) * int(randomitem.product_quantity)
        randomitem.item_price = price_with_gst

        randomitem.save()

        frag["message"] = "Random Item Successfully Updated"
        frag["order_item_price"] = randomitem.item_price
        frag["order_item_gst_price"] = randomitem.item_gst_price
        frag["order_product_price"] = randomitem.product_price
        frag["order_product_quantity"] = randomitem.product_quantity
        return Response(frag, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        try:
             randomitem = RandomItemModel.objects.filter(shop=request.user.shop).get(randomitem_id=request.data.get('orderitem_id'))
        except:
            return Response({'error': 'Random Item Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        randomitem.delete()
        frag = {}
        frag["message"] = "Random Item Successfully Deleted"
        return Response(frag, status=status.HTTP_200_OK)

#########################################################################
##  End RandomItem Features  ##
#########################################################################



#########################################################################


#########################################################################
##  Start Basket Fetaures  ##
#########################################################################
# Place your item on Basket
@api_view(['POST', ])
def BasketListView(request):
    if request.method == 'POST':
        frag = {}
        try:
            order_items = OrderItemModel.objects.filter(shop=request.user.shop).filter(item_status=1)
            random_items = RandomItemModel.objects.filter(shop=request.user.shop).filter(item_status=1)
        except:
            return Response({'error': 'Order / Random Items Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)
        trail = []
        print(order_items)
        for i in range(0, len(order_items)):
            frag['order_item_id'] = order_items[i].orderitem_id
            frag['item_status'] = order_items[i].item_status

            frag['item_name'] = order_items[i].product.product_name
            frag['product_price'] = order_items[i].product.product_mrp_price
            frag['item_price'] = order_items[i].item_price
            frag['item_gst'] = order_items[i].product.product_gst
            frag['item_quantity'] = order_items[i].item_quantity
            trail.append(frag)
            frag = {}

        print(random_items)
        for i in range(0, len(random_items)):
            frag['order_item_id'] = random_items[i].randomitem_id
            frag['item_status'] = random_items[i].item_status
            frag['item_price'] = random_items[i].item_price

            frag['product_price'] = random_items[i].product_price
            frag['item_name'] = random_items[i].product_name
            frag['item_gst'] = random_items[i].product_gst
            frag['item_quantity'] = random_items[i].product_quantity
            trail.append(frag)
            frag = {}

        return Response(trail, status=status.HTTP_200_OK)


#########################################################################
# Checkout the all the unbilled Items
@api_view(['POST', ])
def CheckoutView(request):
    if request.method == 'POST':
        frag={}
        _order_price = 0
        _order_gst_price = 0
        try:
            order_items = OrderItemModel.objects.filter(shop=request.user.shop).filter(item_status=1)
            random_items = RandomItemModel.objects.filter(shop=request.user.shop).filter(item_status=1)
        except:

            return Response({'error': 'Order / Rendom Item Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)
        # 1 : Full Payment -- 2 : Partial Payment
        order_status = int(request.data.get('order_status'))
        
        
        if order_status == 1 or order_status == 2 :
            if(bool(order_items) or bool(random_items)):
                try:
                    customer = CustomerModel.objects.get(customer_id=request.data.get('customer_id'))
                    all_orders = OrderModel.objects.filter(shop=request.user.shop)
                except:
                    return Response({'error': 'Shop / Order Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

                for item in order_items:
                    _order_price += item.item_price
                    _order_gst_price += item.item_gst_price

                for item in random_items:
                    _order_price += item.item_price
                    _order_gst_price += item.item_gst_price
            
                
                # order_discount = int(request.data.get("order_discount"))
                order_discount = 0
                _order_discounted_price = (int(_order_price) * (int(order_discount)/100))
                _order_price = (int(_order_price) - (_order_discounted_price))

                order = OrderModel(
                    shop = request.user.shop,
                    customer = customer,
                    order_no = len(all_orders.all()) + 1,
                    
                    order_price = _order_price,
                    order_gst_price = _order_gst_price,
                    order_discounted_price = _order_discounted_price,

                    order_discount = request.data.get("order_discount"),

                    order_payment = request.data.get("order_payment"),
                    order_status = request.data.get("order_status"),
                    account_type = request.data.get("account_type"),
                )
                if order_status == 1:
                    order.order_balance = 0
                elif order_status == 2:
                    amount_paid = request.data.get('amount_paid')
                    if int(amount_paid) >= int(_order_price):
                        return Response({'error': 'Invalid Billing type or Over Paid'}, status=status.HTTP_403_FORBIDDEN)
                    order.order_balance = _order_price - int(amount_paid)
                else:
                    return Response({'error': 'Invalid Billing type or Over Paid'}, status=status.HTTP_403_FORBIDDEN)

                order.save()

                for item in order_items:
                    order.order_items.add(item)
                    item.item_status = 2
                    item.product.product_stock  -= item.item_quantity
                    item.save()
                    item.product.save()
                order.save()

                for item in random_items:
                    order.random_items.add(item)
                    item.item_status = 2
                    item.save()
                order.save()
                
                # Calcluate the Order Price and Upload to the Table
                trail = []
                order.save()
                frag['order_id'] = order.order_id
                frag['order_price'] = order.order_price
                frag['order_balance'] = order.order_balance

            else:
                frag = {'message': 'No Orders on Progress'}

            return Response(frag, status=status.HTTP_200_OK)

           

        return Response(frag, status=status.HTTP_200_OK)

#########################################################################
##  End Basket Fetaures  ##
#########################################################################



#########################################################################




#########################################################################
#  Purcahse List
@api_view(['POST'])
def SalesListView(request):
    if request.method == 'POST':
        frag = {}
        trail = []
        filter_type = int(request.data.get('filter_type')) 
        try:
            if filter_type == 1: # All Filter
                factors = OrderModel.objects.filter(shop=request.user.shop).order_by('-time_stamp')
            if filter_type == 2: # Till Day Filter
                factors = OrderModel.objects.filter(shop=request.user.shop).order_by('-time_stamp')
            if filter_type == 3: # Range Filter
                factors = OrderModel.objects.filter(shop=request.user.shop).order_by('-time_stamp')
        except:
            return Response({'error': 'Orders Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        for i in range(0, len(factors)):
            frag = {}
            order = factors[i]
            frag['order_id'] = order.order_id

            # Vendor
            frag['customer_name'] = order.customer.customer_name
            frag['customer_mobile'] = order.customer.customer_mobile
            frag['customer_address_1'] = order.customer.customer_address_1
            frag['customer_address_2'] = order.customer.customer_address_2
            frag['customer_address_3'] = order.customer.customer_address_3
            frag['customer_type'] = order.customer.customer_type

            frag['order_no'] = order.order_no
            frag['order_price'] = order.order_price
            frag['order_gst_price'] = order.order_gst_price
            frag['order_discounted_price'] = order.order_discounted_price
            frag['order_balance'] = order.order_balance

            frag['order_status'] = order.order_status
            frag['order_payment'] = order.order_payment
            frag['account_type'] = order.account_type

            frag['time_stamp'] = order.time_stamp


            try:
                order_items = order.order_items.all()
                random_items = order.random_items.all()
            except:
                return Response({'error': 'Order / Random Items Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

            sub_frag = {}
            sub_trail = []
            for item in range(0, len(order_items)):
                current = order_items[item]
                sub_frag['order_item_id'] = current.orderitem_id
                sub_frag['product_name'] = current.product.product_name
                sub_frag['product_vendor_price'] = current.product.product_vendor_price
                sub_frag['product_mrp_price'] = current.product.product_mrp_price
                sub_frag['product_gst'] = current.product.product_gst

                sub_frag['item_price'] = current.item_price
                sub_frag['item_quantity'] = current.item_quantity
                sub_frag['item_status'] = current.item_status

                sub_trail.append(sub_frag)
                sub_frag = {}

            frag['order_items'] = sub_trail  #
            # frag = {}

            sub_frag = {}
            sub_trail = []
            for item in range(0, len(random_items)):
                current = random_items[item]
                sub_frag['order_item_id'] = current.randomitem_id
                sub_frag['product_name'] = current.product_name
                sub_frag['product_price'] = current.product_price
                sub_frag['product_gst'] = current.product_gst
                sub_frag['product_quantity'] = current.product_quantity

                sub_frag['item_status'] = current.item_status
                sub_frag['item_price'] = current.item_price

                sub_trail.append(sub_frag)
                sub_frag = {}
            frag['random_items'] = sub_trail  #
            # frag = {}

            
            
            trail.append(frag)

        return Response(trail, status=status.HTTP_200_OK)


########################################################################
##  End Purchase CRUD Views  ##
#########################################################################