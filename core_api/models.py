from django.db import models

# For Account
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# For Auth Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta

from auth_api.models import *

#################################################################################
class ProductModel(models.Model):
    PRODUCT_TYPE_CHOICES = ((1, 'Gram'), (2, 'Kilo Gram'), (3, 'Piece'),
                            (4, 'Box / Packets'),(5, 'Litre'),(6, 'Milli Litre'))
    PRODUCT_TEMPLATE = ((1, 'Product - Expiry'), (2, 'Product - Non-Expiry'), (3, ' v 2'))

    # Primary Key   
    product_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)

    # Inside Serializers
    shop = models.ForeignKey(ShopModel, on_delete=models.CASCADE,)

    # Active Fields
    product_code = models.CharField(max_length=50, blank=True,null=True)
    product_name = models.CharField(max_length=100, blank=True,null=True)
    product_stock = models.IntegerField(blank=True, null=True,)

    product_vendor_price = models.FloatField(blank=True,null=True)
    product_mrp_price = models.FloatField(blank=True,null=True)
    product_gst = models.FloatField(blank=True, null=True, default=0)

    product_available = models.BooleanField(default=True)

    # Auto add fields
    time_stamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Model"

    def __str__(self):
        return self.shop.shop_name + ' - ' + self.product_name + ' - ' + self.product_code
##################################################################################


##################################################################################
class OrderItemModel(models.Model):
    ITEM_STATUS_CHOICES = ((1, 'Un-billed'), (2, 'Billed'))

    # Primary Key
    orderitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Inside Serializers
    shop = models.ForeignKey(ShopModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    # Active Fields
    item_price = models.FloatField()
    item_gst_price = models.FloatField()
    item_quantity = models.IntegerField()

    # Advance Feature
    item_status = models.PositiveSmallIntegerField(choices=ITEM_STATUS_CHOICES, null=True, default=1)

    # Auto add fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Order Item Model"

    def __str__(self):
        return self.shop.shop_name + ' - ' + self.product.product_name + " - " + str(self.item_quantity)
##################################################################################


##################################################################################
class RandomItemModel(models.Model):
    ITEM_STATUS_CHOICES = ((1, 'Un-billed'), (2, 'Billed'))

    # Primary Key
    randomitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Inside Serializers
    shop = models.ForeignKey(ShopModel, on_delete=models.CASCADE)

    # Active Fields
    product_name = models.CharField(max_length=100)
    product_gst = models.IntegerField(default=None, null=True, blank=True)
    product_price = models.FloatField(default=None,null=True, blank=True)
    product_quantity = models.IntegerField(default=None)

    # Advance Feature
    item_price = models.FloatField()
    item_gst_price = models.FloatField()
    item_status = models.PositiveSmallIntegerField(choices=ITEM_STATUS_CHOICES, null=True, default=1)

    # Auto add fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Random Item Model"

    def __str__(self):
        return self.shop.shop_name + ' - ' + self.product_name + " - " + str(self.product_quantity)
##################################################################################


##################################################################################
class OrderModel(models.Model):
    ORDER_STATUS_CHOICES = ((1,'Fully Payment'),(2, 'Partial Payment'))
    ORDER_PAYMENT_CHOICES = ((1, 'Online'), (2, 'Cash'), (2, 'Not Paid'))
    ACCOUNT_CHOICES = ((1, 'Billed'), (2, 'Not Billed'), (2, 'Temp'))

    # Primary Key
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    # Inside Serializer
    shop = models.ForeignKey(ShopModel, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, blank=True, null=True)

    # Many-to-many Fields
    order_items = models.ManyToManyField(OrderItemModel)
    random_items = models.ManyToManyField(RandomItemModel)

    order_no = models.PositiveSmallIntegerField(null=True, blank=True)

    order_price = models.FloatField(null=True, blank=True)
    order_gst_price = models.FloatField(null=True, blank=True)
    order_discounted_price = models.FloatField(null=True, blank=True)

    order_discount = models.PositiveIntegerField(null=True, blank=True, default=0)
    order_balance = models.PositiveIntegerField(null=True, blank=True)

    order_status = models.PositiveSmallIntegerField(choices=ORDER_STATUS_CHOICES,null=True, default=1)
    order_payment = models.PositiveSmallIntegerField(choices=ORDER_PAYMENT_CHOICES, null=True, default=1)

    coupoun_applied = models.BooleanField(default=False)
    account_type = models.PositiveSmallIntegerField(choices=ACCOUNT_CHOICES, null=True, default=1)

    # Auto add fields
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order Model"

    def __str__(self):
        return str(self.order_price)
##################################################################################



##################################################################################
class CoupounModel(models.Model):
    ITEM_STATUS_CHOICES = ((1, 'Type1'), (2, 'Type2'))

    # Primary Key
    coupoun_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Inside Serializers
    shop = models.ForeignKey(ShopModel, on_delete=models.CASCADE)

    # Active Fields
    coupoun_code = models.CharField(max_length=10, blank=True,null=True)
    coupoun_description = models.CharField(max_length=100, blank=True,null=True)

    coupoun_min_value = models.FloatField()
    coupoun_discount = models.FloatField()
    coupoun_max_discount = models.FloatField()
    coupoun_limit = models.IntegerField()
    coupoun_remaining_limit = models.IntegerField()
    coupoun_expiry = models.DateTimeField()

    # Advance Feature
    coupoun_type = models.PositiveSmallIntegerField(choices=ITEM_STATUS_CHOICES, null=True, default=1)

    # Auto add fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Coupoun Model"

    def __str__(self):
        return self.coupoun_code
##################################################################################

