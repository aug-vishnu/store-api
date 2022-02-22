from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from core_api.models import *
# from invoice_api.models import *
from core_api.serializers import *

# from core_api.send_mail import send_mail


#########################################################################
##  Start Invoice Detail  ##
#########################################################################
#  Invoice Detail

@api_view(['POST', ])
def InvoicedetailView(request):
    if request.method == 'POST':
        PRODUCT_TYPE_CHOICES = ((1, 'Gram'), (2, 'Kilo Gram'), (3, 'Piece'),
                            (4, 'Box / Packets'),(5, 'Litre'),(6, 'Milli Litre'))

        frag={}
        order_gst_price = 0
        print(request.data)
        try:
            shop = request.user.shop
            all_orders = OrderModel.objects.filter(shop = shop)
            factor = OrderModel.objects.filter(shop = shop).get(order_id = request.data.get('order_id'))
            # content = InvoiceContentModel.objects.get(shop = shop)
        except:
            return Response({'error': 'Orders Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)
        
        trail = []
        #  Shop details
        frag['shop_name'] = shop.shop_name
        frag['shop_mobile'] = shop.shop_mobile
        frag['shop_name'] = shop.shop_name
        frag['shop_address_1'] = shop.shop_address
        frag['shop_address_2'] = shop.shop_address_2
        frag['shop_address_3'] = shop.shop_address_3
        # frag['invoice_prefix'] = shop.invoice_prefix
        frag['gsit'] = shop.gsit
        frag['shop_logo'] = shop.shop_logo
        # frag['invoice_design'] = shop.invoice_design.invoice_design_html
        # frag['invoice_design_id'] = shop.invoice_design.invoice_design_id
        # frag['invoice_design_code'] = shop.invoice_design.invoice_design_code

        # Shop Content
        # frag['design_types'] = content.design_types
        # frag['invoice_header1'] = content.invoice_header1
        # frag['invoice_header2'] = content.invoice_header2
        # frag['invoice_header3'] = content.invoice_header3
        # frag['invoice_footer1'] = content.invoice_footer1
        # frag['invoice_footer2'] = content.invoice_footer2
        # frag['invoice_footer3'] = content.invoice_footer3
        # frag['invoice_misc1'] = content.invoice_misc1
        # frag['invoice_misc2'] = content.invoice_misc2
        # frag['invoice_misc3'] = content.invoice_misc3


        # Shop Owner Details
        owners = AdminModel.objects.filter(shop=shop)
        frag['owner_name'] = owners[0].user.email
        frag['owner_number'] = owners[0].user.mobile_number
        
        # Order Customer Details
        frag['customer_id'] = factor.customer.customer_id
        frag['customer_name'] = factor.customer.customer_name
        frag['customer_address_1'] = factor.customer.customer_address_1
        frag['customer_address_2'] = factor.customer.customer_address_2
        frag['customer_address_3'] = factor.customer.customer_address_3
        frag['customer_type'] = factor.customer.customer_type
        frag['customer_mobile'] = factor.customer.customer_mobile

        # Bank details
        # bank = BankdetailModel.objects.get(shop=shop)
        # frag['bank_name'] = bank.bank_name
        # frag['bank_account_no'] = bank.bank_account_no
        # frag['bank_branch'] = bank.bank_branch
        # frag['bank_ifsc'] = bank.bank_ifsc

        frag['order_no'] = factor.order_no
        frag['no_products'] = len(factor.order_items.all())
        
        frag['order_price'] = factor.order_price
        frag['order_price'] = factor.order_discounted_price
        frag['order_balance'] = factor.order_balance
        frag['order_discount'] = factor.order_discount

        frag['order_status'] = factor.order_status
        frag['order_payment'] = factor.order_payment
        frag['time_stamp'] = factor.time_stamp

        # trail.append(frag)
        # frag = {}

        try:
            order_items = factor.order_items.all()
            random_items = factor.random_items.all()
        except:
            return Response({'error': 'Order / Random Items Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        sub_frag = {}
        # frag = {}
        sub_trail = []
        for item in range(0, len(order_items)):
            current = order_items[item]
            sub_frag['order_item_id'] = current.orderitem_id
            sub_frag['product_name'] = current.product.product_name
            sub_frag['product_quantity'] = current.item_quantity
            sub_frag['product_code'] = current.product.product_code
            # if current.product.product_value:
            #     print(PRODUCT_TYPE_CHOICES[current.product.product_type-1])
            #     sub_frag['product_quantity_value'] = (str(current.item_quantity * int(current.product.product_value)) + ' ' + PRODUCT_TYPE_CHOICES[current.product.product_type-1][1]) 

            sub_frag['product_price'] = current.product.product_mrp_price
            sub_frag['product_gst_price'] = (current.product.product_mrp_price * current.item_quantity) * (current.product.product_gst / 100)
            order_gst_price += (current.product.product_mrp_price * current.item_quantity) * (current.product.product_gst / 100)
            sub_frag['product_gst'] = current.product.product_gst
            sub_frag['product_sgst'] = current.product.product_gst / 2

            sub_frag['item_price'] = current.item_price
            sub_frag['item_status'] = current.item_status

            sub_trail.append(sub_frag)
            sub_frag = {}
        frag['order_items'] = sub_trail
        # trail.append(frag)
        # frag = {}

        sub_frag = {}
        sub_trail = []
        for item in range(0, len(random_items)):
            current = random_items[item]
            sub_frag['order_item_id'] = current.randomitem_id
            sub_frag['product_name'] = current.product_name
            sub_frag['product_quantity'] = current.product_quantity
            
            sub_frag['product_price'] = current.product_price
            sub_frag['product_gst_price'] = (current.product_price * current.product_quantity) * (current.product_gst / 100)
            order_gst_price += (current.product_price * current.product_quantity) * (current.product_gst / 100)

            sub_frag['product_gst'] = current.product_gst
            sub_frag['product_sgst'] = current.product.product_gst / 2

            sub_frag['item_status'] = current.item_status
            sub_frag['item_price'] = current.item_price

            sub_trail.append(sub_frag)
            sub_frag = {}
        frag['random_items'] = sub_trail
        frag['order_gst_price'] = order_gst_price
        frag['amount_paid'] = factor.order_price - factor.order_balance
        frag['order_wo_gst_price'] = factor.order_price - order_gst_price 

        # order_price_text = num2words(factor.order_price, lang = 'en_IN')
        # print(order_price_text)
        # frag['order_price_text'] = order_price_text

        trail.append(frag)
        frag = {}

    return Response(trail, status=status.HTTP_200_OK)


#########################################################################
##  End Invoice Detail  ##
#########################################################################

