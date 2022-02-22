import random,math
from rest_framework import serializers
from datetime import datetime,timedelta
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
import string

from auth_api.models import *
from core_api.models import *


##################################################################################
##################################################################################
class ShopCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = ShopModel
        fields = ['email','password','shop_name','shop_address','shop_mobile','subscription_type','subscription_start','subscription_end']


    def save(self, user):

        six_digit_code = get_random_string(7, allowed_chars=string.ascii_uppercase + string.digits)
        dupe_sites = ShopModel.objects.filter(shop_license = six_digit_code)
        while(len(dupe_sites) != 0):
            print(len(dupe_sites))
            dupe_sites = ShopModel.objects.filter(shop_license = six_digit_code)
            six_digit_code = get_random_string(7, allowed_chars=string.ascii_uppercase + string.digits)
            print(six_digit_code)

        new_object = ShopModel(
            shop_name = self.validated_data['shop_name'],
            shop_address = self.validated_data['shop_address'],
            shop_mobile = self.validated_data['shop_mobile'],
            subscription_type = self.validated_data['subscription_type'],
            subscription_start = self.validated_data['subscription_start'],
            subscription_end = self.validated_data['subscription_end'],
            shop_license = six_digit_code,
            )
        new_object.save()

        email=self.validated_data['email'].lower(),
        username=self.validated_data['email'].lower(),
        account = Account(
            email=email[0],
            username=username[0],
            user_type = 1, 
            shop = new_object,
        )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
       
        owner_object = AdminModel(
            shop = new_object,
            user = account,
        )

        owner_object.save()

        return new_object

##################################################################################
class ShopEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopModel
        fields = ['shop_name','shop_address','shop_mobile','subscription_type','subscription_start','subscription_end']



class SubAdminPermissionEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubadminPermisionModel
        fields = '__all__'



##################################################################################
##################################################################################


##################################################################################


##################################################################################
##################################################################################

class AdminCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email','password',]


    def save(self,user):
        email=self.validated_data['email'].lower(),
        username=self.validated_data['email'].lower(),
        new_object = Account(
            email=email[0],
            username=username[0],
            user_type = 1, 
        )
        password = self.validated_data['password']
        new_object.set_password(password)
       
        try:
            owner = AdminModel.objects.get(user = user)
        except:
            raise serializers.ValidationError('Not Authorized')

        new_object.save()

        owner_object = AdminModel(
            # shop = SiteModel.objects.get(shop_id =  self.validated_data['shop']),
            shop = owner.shop,
            user = new_object,
        )

        owner_object.save()

        return new_object
##################################################################################
class AdminEditSerializer(serializers.ModelSerializer):   
    
    class Meta:
        model = AdminModel
        fields = ['owner_name','owner_address','owner_mobile']

##################################################################################
##################################################################################


##################################################################################


##################################################################################
##################################################################################
class SubAdminCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email','password']

    def save(self,user):
        email=self.validated_data['email'].lower(),
        username=self.validated_data['email'].lower(),
        new_object = Account(
            shop = user.shop,
            email=email[0],
            username=username[0],
            user_type = 2, 
        )
        password = self.validated_data['password']

        new_object.set_password(password)
        print(user)
        # try:
        #     owner = AdminModel.objects.get(user = user)
        # except:
        #     raise serializers.ValidationError('Not Authorized')

        new_object.save()

        manager = SubAdminModel(
            shop = user.shop,
            user= new_object,
        )
        manager.save()

        # Activity
        activity = ActivityModel.objects.create(
            shop = user.shop,
            activity_comment = 'SubAdmin with username : ' + new_object.username + ' account was created by ' + user.username ,
            activity_type = 1
        )
        
        return new_object
##################################################################################
class SubAdminEditSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubAdminModel
        fields = ['manager_name','manager_address','manager_mobile']

##################################################################################
##################################################################################


##################################################################################
    
    
##################################################################################
##################################################################################
class CustomerCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = CustomerModel
        fields = ['email','password','customer_name','customer_type','customer_mobile','customer_address_1','customer_address_2','customer_address_3',]

    def save(self, shop):
        # try:
        #     official = AdminModel.objects.get(user = user)
        # except:
        #     try:
        #         official = SubAdminModel.objects.get(user = user)
        #     except:
        #         raise serializers.ValidationError('Not Authorized')

        email=self.validated_data['email'].lower(),
        username=self.validated_data['email'].lower(),
        user = Account(
            shop = shop,
            email=email[0],
            username=username[0],
            user_type = 4, 
        )
        password = self.validated_data['password']

        user.set_password(password)
        user.save()

        new_object = CustomerModel(
            shop = shop,
            user=user,
            customer_name = self.validated_data['customer_name'],
            customer_mobile = self.validated_data['customer_mobile'],
            customer_type = self.validated_data['customer_type'],
            customer_address_1 = self.validated_data['customer_address_1'],
            customer_address_2 = self.validated_data['customer_address_2'],
            customer_address_3 = self.validated_data['customer_address_3'],

            )
        new_object.save()
        BlendingOptionsModel.create(
            customer = new_object
        )
        # Activity
        # if user.user_type  == 2:
        #     activity = ActivityModel.objects.create(
        #         shop = user.shop,
        #         activity_comment = 'Customer : ' + new_object.company_name + ' - ' + new_object.customer_name + '  was created by ' + user.username ,
        #         activity_type = 1
        #     )

        return new_object

##################################################################################
class CustomerEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ['customer_name','customer_mobile','customer_address_1','customer_type','customer_address_2','customer_address_3',]
##################################################################################
##################################################################################


##################################################################################
    
    
# ##################################################################################
# ##################################################################################
# class DistributorCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DistributorModel
#         fields = ['distributor_name','distributor_mobile','distributor_address']

#     def save(self, user):
#         try:
#             official = AdminModel.objects.get(user = user)
#         except:
#             try:
#                 official = SubAdminModel.objects.get(user = user)
#             except:
#                 raise serializers.ValidationError('Not Authorized')


#         new_object = DistributorModel(
#             shop = official.shop,
#             distributor_name = self.validated_data['distributor_name'],
#             distributor_mobile = self.validated_data['distributor_mobile'],
#             distributor_address = self.validated_data['distributor_address'],
#             )
#         new_object.save()
#         # Activity
#         if user.user_type  == 2:
#             activity = ActivityModel.objects.create(
#                 shop = user.shop,
#                 activity_comment = 'Distributor : ' + new_object.company_name + ' - ' + new_object.distributor_name + '  was created by ' + user.username ,
#                 activity_type = 1
#             )
#         return new_object

# ##################################################################################
# class DistributorEditSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DistributorModel
#         fields = ['distributor_name','distributor_mobile','distributor_address']
# ##################################################################################
# ##################################################################################


##################################################################################


##################################################################################
##################################################################################
class ResetPasswordSerializer(serializers.ModelSerializer):
    
    password_confirm = serializers.CharField()
    password_old = serializers.CharField()
    class Meta:
        model = Account
        fields = ['password_old','password_confirm','password']

    def save(self,account):
        password = self.validated_data['password']
        password_old = self.validated_data['password_old']
        password_confirm = self.validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'message':'Password Doesn\'t match'})
        if not account.check_password(password_old):
            raise serializers.ValidationError({'message':'Old Password Doesn\'t Correct'})

        account.set_password(password)
        account.save()
        return account
##################################################################################
##################################################################################


##################################################################################


##################################################################################
##################################################################################
class ForgotPasswordSerializer(serializers.ModelSerializer):
    
    password_confirm = serializers.CharField()
    forgot_otp = serializers.CharField()
    class Meta:
        model = Account
        fields = ['forgot_otp','password_confirm','password']



    def save(self,account):
        password = self.validated_data['password']
        forgot_otp = self.validated_data['forgot_otp']
        password_confirm = self.validated_data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({'message':'Password Doesn\'t match'})

        forgotToken = ForgotTokens.objects.filter(user=account.user_id).order_by('-created_time')
        expiry=forgotToken[0].expiry_time
        now=timezone.now()
        diff=(expiry-now).total_seconds()
        remaining=divmod(diff,60)[0]
        if int(remaining) < 1.0:
            raise serializers.ValidationError({'message':'Provided OTP Expired'})

        if int(forgotToken[0].forgot_otp) != int(forgot_otp):
            raise serializers.ValidationError({'message':'Provided OTP Doesn\'t Correct'})

        # if not account.check_password(password_old):
        account.set_password(password)
        account.save()
        return account
##################################################################################
##################################################################################



