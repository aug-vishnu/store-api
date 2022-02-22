from rest_framework import serializers
import random
import math

#  For Mail
from django.core.mail import send_mail

# For SMS
from django.conf import settings

from auth_api.models import *
from core_api.models import *


#########################################################################
##  Start Product CRUD  ##
#########################################################################
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['product_name', 'product_stock', 'product_gst', 
        'product_code', 'product_vendor_price', 'product_mrp_price',]

    def save(self, user):

        #########################################################################
        try:
            # CODE#DOCKTROLES
            shop = user.shop

        except:
            raise serializers.ValidationError('Admin / Shop Not Found in Serializer')
        #########################################################################
        product = ProductModel(
                        shop=shop,
                        product_code=self.validated_data['product_code'],
                        product_name=self.validated_data['product_name'],
                        product_stock=self.validated_data['product_stock'],

                        product_vendor_price=self.validated_data['product_vendor_price'],
                        product_mrp_price=self.validated_data['product_mrp_price'],
                        product_gst=self.validated_data['product_gst'],
                    )
        product.save()
        print(product.product_mrp_price)
        
        return product



#########################################################################

class EditProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['product_name', 'product_stock', 'product_gst', 'product_code', 'product_vendor_price', 'product_mrp_price','product_available']



#########################################################################
##  End Product CRUD  ##
#########################################################################


#########################################################################


#########################################################################
#########################################################################
class OrderItemCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItemModel
        fields = ['product', 'item_quantity']

    def save(self, user):

        #########################################################################
        try:
            # CODE#DOCKTROLES
            shop = user.shop
        except:
            raise serializers.ValidationError('Admin / Shop Not Found in Serializer')
        #########################################################################

        product = self.validated_data['product']

        price_with_gst = (product.product_mrp_price + (product.product_mrp_price * (product.product_gst/100))) * self.validated_data['item_quantity']
        gst_price = (product.product_mrp_price * (product.product_gst/100))
        print(price_with_gst)

        orderitem = OrderItemModel(
            shop=shop, 
            product=product,
            item_status=1,

            item_quantity=self.validated_data['item_quantity'],
            item_price=price_with_gst,
            item_gst_price=gst_price,
            )
        orderitem.save()
        return orderitem
#########################################################################

#########################################################################
class RandomItemCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RandomItemModel
        fields = ['product_quantity', 'product_gst', 'product_name', 'product_price']

    def save(self, user):

        #########################################################################
        try:
            # CODE#DOCKTROLES
            shop = user.shop
        except:
            raise serializers.ValidationError('Admin / Shop Not Found in Serializer')
        #########################################################################

        product_price = self.validated_data['product_price']
        product_gst = self.validated_data['product_gst']
        product_quantity = self.validated_data['product_quantity']

        price_with_gst = (int(product_price) + (int(product_price) * (int(product_gst)/100))) * int(product_quantity)
        gst_price = (int(product_price) * (int(product_gst)/100))
        print(price_with_gst)
        item_price = price_with_gst
        new_object = RandomItemModel(
            shop=shop, 
            item_status=1,
            product_name = self.validated_data['product_name'],
            product_quantity=self.validated_data['product_quantity'],
            product_gst = self.validated_data['product_gst'],

            item_price=price_with_gst,
            item_gst_price=gst_price
            )
        new_object.save()
        return new_object
#########################################################################

#########################################################################




#########################################################################
##  Start Coupoun CRUD  ##
#########################################################################
class CoupounCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoupounModel
        fields = ['coupoun_code', 'coupoun_description', 'coupoun_min_value', 
        'coupoun_discount', 'coupoun_max_discount', 'coupoun_limit','coupoun_expiry']

    def save(self, user):

        #########################################################################
        try:
            # CODE#DOCKTROLES
            shop = user.shop
        except:
            raise serializers.ValidationError('Admin / Shop Not Found in Serializer')
        #########################################################################
        product = CoupounModel(
                        shop=shop,
                        coupoun_code=self.validated_data['coupoun_code'],
                        coupoun_description=self.validated_data['coupoun_description'],

                        coupoun_min_value=self.validated_data['coupoun_min_value'],
                        coupoun_discount=self.validated_data['coupoun_discount'],
                        coupoun_max_discount=self.validated_data['coupoun_max_discount'],
                        coupoun_limit=self.validated_data['coupoun_limit'],
                        coupoun_remaining_limit=self.validated_data['coupoun_limit'],
                        coupoun_expiry=self.validated_data['coupoun_expiry'],
                    )
        product.save()
        print(product.coupoun_limit)
        
        return product



#########################################################################

class EditCoupounSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoupounModel
        fields = '__all__'

class EditOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlendingOptionsModel
        fields = '__all__'
#########################################################################
##  End Product CRUD  ##
#########################################################################


class ResetPasswordSerializer(serializers.ModelSerializer):
    
    password_confirm = serializers.CharField()
    password_old = serializers.CharField()

    class Meta:
        model = Account
        fields = ['password_old', 'password_confirm', 'password']

    def save(self, account):
        password = self.validated_data['password']
        password_old = self.validated_data['password_old']
        password_confirm = self.validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError(
                {'password': 'Password Doesnt match'})
        if not account.check_password(password_old):
            raise serializers.ValidationError(
                {'password': 'Old Password Doesnt Correct'})

        account.set_password(password)
        account.save()
        return account


class WhoamISerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'user_type']
