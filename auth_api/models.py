from django.db import models

# For Account
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# For Auth Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime,timedelta

from core_api.models import *


##################################################################################
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user
##################################################################################



##################################################################################
# Shop Model
class ShopModel(models.Model):
    SUBSCRIPTION_TYPE = ((1,'Sub 1'),(2,'Sub 2'))
    SHOP_TYPE = ((1,'Eegai Only'),(2,'Dockt Only'),(3,'Both Eegai and Dockt'))

    shop_id = models.UUIDField(primary_key=True,
                                 default=uuid.uuid4,
                                 editable=False)

    # Inside Serializers
    shop_name = models.CharField(max_length=50, blank=True, null=True)
    shop_address = models.CharField(max_length=200, blank=True, null=True)
    shop_mobile = models.CharField(max_length=30, blank=True, null=True)
    shop_logo = models.CharField(max_length=500, blank=True, null=True)
    
    # For Saas
    shop_active = models.BooleanField(default=False)
    shop_license = models.CharField(max_length=7, unique=True ,blank=True, null=True)
    shop_type = models.SmallIntegerField(choices=SHOP_TYPE, default=1)
    subscription_type = models.SmallIntegerField(choices=SUBSCRIPTION_TYPE, default=1)
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)

    # Dockt Fields
    shop_address_2 = models.CharField(max_length=100, blank=True, null=True)
    shop_address_3 = models.CharField(max_length=100, blank=True, null=True)
    gsit = models.CharField(max_length=50, blank=True, null=True)

    # Auto add Fields
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Shop Model"

    def __str__(self):
        return self.shop_name

##################################################################################



##################################################################################
# ShopPermission Model
class ShopPermissionModel(models.Model):
    shop = models.OneToOneField(ShopModel, on_delete=models.CASCADE, blank=True, null=True)

    # Inside Serializers
    parmission1 = models.BooleanField(default=False)
    parmission2 = models.BooleanField(default=False)
    parmission3 = models.BooleanField(default=False)
    parmission4 = models.BooleanField(default=False)
    parmission5 = models.BooleanField(default=False)
    parmission6 = models.BooleanField(default=False)
    parmission7 = models.BooleanField(default=False)

    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Shop Permission Model"

    def __str__(self):
        return self.shop.shop_name

##################################################################################




##################################################################################
# Account Model
class Account(AbstractBaseUser):
    USER_TYPE_CHOICES = ((1,'Admin'),(2,'Sub Admin'),(3,'Distributor'),(4,'Customer'))

    # Primary Key
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Active Fields
    email 					= models.CharField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30,)
    mobile_number 			= models.CharField(max_length=10, blank=True, null=True)
    user_type               = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,null=True)
    shop = models.ForeignKey(ShopModel, on_delete=models.CASCADE, blank=True, null=True)

    # Useless Fields
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_superuser			= models.BooleanField(default=False)
    is_admin				= models.BooleanField(default=False)
    is_staff				= models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


# For Token If place this it will create Tokens By default
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user = instance)
##################################################################################


##################################################################################
# Admin Model
class AdminModel(models.Model):
    # Primary Key
    admin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Inside Serializers
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopModel ,on_delete=models.CASCADE)

    # Active Fields
    admin_name = models.CharField(max_length=20, blank=True, null=True)
    admin_address = models.CharField(max_length=100, blank=True, null=True)
    admin_mobile = models.CharField(max_length=100, blank=True, null=True)


    # Auto add Fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = "Admin Model"
    def __str__(self):
        return self.shop.shop_name + ' - ' + self.user.username
##################################################################################


##################################################################################
# SubAdmin Model
class SubAdminModel(models.Model):
    # Primary Key
    sub_admin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Inside Serializers
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopModel ,on_delete=models.CASCADE)

    # Active Fields
    sub_admin_name = models.CharField(max_length=20, blank=True, null=True)
    sub_admin_address = models.CharField(max_length=100, blank=True, null=True)
    sub_admin_mobile = models.CharField(max_length=100, blank=True, null=True)


    # Auto add Fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = "Sub-admin Model"
    def __str__(self):
        return self.shop.shop_name + ' - ' + self.user.username
##################################################################################

##################################################################################
# Distributor Model
class DistributorModel(models.Model):
    # Primary Key
    distributor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Inside Serializers
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopModel ,on_delete=models.CASCADE)
    
    # Active Fields
    distributor_name = models.CharField(max_length=20, blank=True, null=True)
    distributor_address = models.CharField(max_length=100, blank=True, null=True)
    distributor_mobile = models.CharField(max_length=100, blank=True, null=True)

    # Auto add Fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = "Distributor Model"
    def __str__(self):
        return self.shop.shop_name + ' - ' + self.user.username
##################################################################################


##################################################################################
# Customer Model
class CustomerModel(models.Model):
    CUSTOMER_TYPES = ((1,'Customer'),(2,'Distributor'))

    # Primary Key
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Inside Serializers
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopModel ,on_delete=models.CASCADE)
    
    # Active Fields
    customer_name = models.CharField(max_length=50, blank=True, null=True)
    customer_mobile = models.CharField(max_length=100, blank=True, null=True)
    customer_address_1 = models.CharField(max_length=100, blank=True, null=True)
    customer_address_2 = models.CharField(max_length=100, blank=True, null=True)
    customer_address_3 = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.PositiveSmallIntegerField(choices=CUSTOMER_TYPES, null=True)

    customer_balance = models.IntegerField(default=0)

    # Auto add Fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = "Customer Model"
    def __str__(self):
        return self.shop.shop_name + ' - ' + str(self.customer_name)
##################################################################################


##################################################################################
# BlendingOptions Model
class BlendingOptionsModel(models.Model):
    # Primary Key
    options_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Inside Serializers
    customer = models.ForeignKey(CustomerModel,on_delete=models.CASCADE)
    
    # Active Fields
    blending_option_1 = models.CharField(max_length=100, blank=True, null=True)
    blending_option_2 = models.CharField(max_length=100, blank=True, null=True)
    blending_option_3 = models.CharField(max_length=100, blank=True, null=True)

    # Auto add Fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = "Blending Options Model"
    def __str__(self):
        return str(self.customer.customer_name)
##################################################################################


##################################################################################
# Forgot Token Models
class ForgotTokenModel(models.Model):

    def now_plus_30():
        return datetime.now() + timedelta(minutes=30)

    # Inside Serializers
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    shop = models.OneToOneField(ShopModel ,on_delete=models.CASCADE)

    # In Progran
    created_time = models.DateTimeField(default=datetime.now, blank=True)
    expiry_time = models.DateTimeField(default=now_plus_30 , blank=True)
    forgot_otp = models.PositiveSmallIntegerField()

    # Auto add Fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = "Forgot Token"
    def __str__(self):
        return self.shop.shop_name + ' - ' + self.user.username
##################################################################################


##################################################################################
# SubadminPermision Model
class SubadminPermisionModel(models.Model):
    # SubadminPermision Status
    PERMISSION_TYPES = ((1,'All Acess'),(2,'Create Retrive Update'),(3,'Create Retrive'),(4,'Retrive'),(5,'No Access'))

    # Primary Key
    manager_permission_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Inside Serializers
    shop = models.OneToOneField(ShopModel ,on_delete=models.CASCADE, null=True, blank=True)

    # Factors
    # user_database = models.PositiveSmallIntegerField(choices=PERMISSION_TYPES, null=True)
    # lead_followup = models.PositiveSmallIntegerField(choices=PERMISSION_TYPES, null=True)
    # invoice_followup = models.PositiveSmallIntegerField(choices=PERMISSION_TYPES, null=True)
    # task_followup = models.PositiveSmallIntegerField(choices=PERMISSION_TYPES, null=True)
    # journal = models.PositiveSmallIntegerField(choices=PERMISSION_TYPES, null=True)

    # Auto add Fields
    time_stamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name = "Manager Permision Model"
    def __str__(self):
        return self.shop.shop_name 
##################################################################################