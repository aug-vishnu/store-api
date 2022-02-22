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
# Start Admin CRUD
#########################################################################
@api_view(['POST','PUT', 'DELETE' ])
def AdminCUDView(request):
    trail = {}

    # Create Admin
    if request.method == 'POST':
        serializer = AdminCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_object = serializer.save(user=request.user)
            trail['message'] = "Admin Sucessfully Created"
            trail["data"] =  serializer.data
            return Response(trail, status=status.HTTP_200_OK)

        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)


    # Edit Admin
    if request.method == 'PUT':
        try:
            owner = AdminModel.objects.get(admin_id=request.data.get("admin_id"))
        except:
            raise serializers.ValidationError('Not Found')

        serializer = AdminEditSerializer(owner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            trail["message"] = "Admin Successfully Updated"
            trail["data"] =  serializer.data
            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)
        
    # Delet Admin
    if request.method == 'DELETE':
        try:
            owner = AdminModel.objects.get(admin_id=request.data.get("admin_id"))
        except:
            raise serializers.ValidationError('Not Found')
        owner.delete()
        owner.user.delete()
        trail["message"] = "Admin Successfully Deleted"
        return Response(trail, status=status.HTTP_200_OK)
        
#########################################################################


#########################################################################
# Admin List from app
@api_view(['POST', ])
def AdminListView(request):
    if request.method == 'POST':
        try:
            owner = AdminModel.objects.get(user = request.user)
            factors = AdminModel.objects.filter(shop = owner.shop)
        except:
            raise serializers.ValidationError('Not Authorized')

        trail = []
        frag = {}
        for i in range(0, len(factors)):
            frag['shop_name'] = factors[i].shop.shop_name
            frag['shop_id'] = factors[i].shop.shop_id
            frag['admin_id'] = factors[i].admin_id
            frag['username'] = factors[i].user.username

            trail.append(frag)
            frag = {}
        return Response(trail)
        
#########################################################################


#########################################################################
# Admin Detail from app
@api_view(['POST', ])
def AdminDetailView(request):
    if request.method == 'POST':
        factor = AdminModel.objects.filter(shop = request.user.shop).get(admin_id = request.data.get('admin_id'))
        frag = {}
        frag['admin_id'] = factor.admin_id
        frag['admin_name'] = factor.user.username
        frag['shop_name'] = factor.shop.shop_name
        frag['shop_id'] = factor.shop.shop_id
        return Response(frag)

#########################################################################
##  End Admin CRUD  ##
#########################################################################


#########################################################################


#########################################################################
# Start SubAdmin CRUD
#########################################################################
@api_view(['POST','PUT', 'DELETE' ])
def SubAdminCUDView(request):
    trail = {}

    # Create SubAdmin
    if request.method == 'POST':
        serializer = SubAdminCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_object = serializer.save(user=request.user)
            trail['message'] = "SubAdmin Sucessfully Created"
            manager = SubAdminModel.objects.get(user = new_object)
            trail["sub_admin_id"] =  manager.sub_admin_id

            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)

    # Edit SubAdmin
    if request.method == 'PUT':
        try:
            factor = SubAdminModel.objects.filter(shop = request.user.shop).get(sub_admin_id = request.data.get('sub_admin_id'))        
        except:
            raise serializers.ValidationError('Not Found')

        serializer = SubAdminEditSerializer(factor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            trail["message"] = "SubAdmin Successfully Updated"
            trail["data"] =  serializer.data
            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)
        
    # Delet SubAdmin
    if request.method == 'DELETE':
        try:
            factor = SubAdminModel.objects.filter(shop = request.user.shop).get(sub_admin_id = request.data.get('sub_admin_id'))
        except:
            raise serializers.ValidationError('Not Found')
        factor.delete()
        factor.user.delete()
        trail["message"] = "SubAdmin Successfully Deleted"
        return Response(trail, status=status.HTTP_200_OK)
        
#########################################################################


#########################################################################
# SubAdmin List from app
@api_view(['POST', ])
def SubAdminListView(request):
    if request.method == 'POST':
        try:
            factors = SubAdminModel.objects.filter(shop = request.user.shop)
        except:
            raise serializers.ValidationError('Not Authorized')

        trail = []
        frag = {}
        for i in range(0, len(factors)):
            frag['sub_admin_name'] = factors[i].sub_admin_name
            frag['username'] = factors[i].user.username
            frag['shop_name'] = factors[i].shop.shop_name
            frag['shop_id'] = factors[i].shop.shop_id
            frag['sub_admin_id'] = factors[i].sub_admin_id
            frag['sub_admin_address'] = factors[i].sub_admin_address
            frag['sub_admin_mobile'] = factors[i].sub_admin_mobile
            frag['sub_admin_id'] = factors[i].sub_admin_id

            trail.append(frag)
            frag = {}
        return Response(trail)
        
#########################################################################


#########################################################################
# SubAdmin Detail from app
@api_view(['POST', ])
def SubAdminDetailView(request):
    if request.method == 'POST':
        factor = SubAdminModel.objects.filter(shop = request.user.shop).get(sub_admin_id = request.data.get('sub_admin_id'))
        frag = {}
        frag['username'] = factor.user.username
        frag['sub_admin_name'] = factor.sub_admin_name
        frag['shop_name'] = factor.shop.shop_name
        frag['shop_id'] = factor.shop.shop_id
        frag['sub_admin_id'] = factor.sub_admin_id
        frag['sub_admin_address'] = factor.sub_admin_address
        frag['sub_admin_mobile'] = factor.sub_admin_mobile
        frag['sub_admin_id'] = factor.sub_admin_id

        return Response(frag)

#########################################################################
##  End SubAdmin CRUD  ##
#########################################################################


#########################################################################


#########################################################################
# Start Distributor CRUD
#########################################################################
@api_view(['POST','PUT', 'DELETE' ])
def DistributorCUDView(request):
    trail = {}

    # Create Distributor
    if request.method == 'POST':
        serializer = DistributorCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_object = serializer.save(user=request.user)
            trail['message'] = "Distributor Sucessfully Created"
            trail["data"] =  serializer.data

            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)


    # Edit Distributor
    if request.method == 'PUT':
        try:
            factor = DistributorModel.objects.filter(shop = request.user.shop).get(distributor_id = request.data.get('distributor_id'))        
        except:
            raise serializers.ValidationError('Not Found')

        serializer = DistributorEditSerializer(factor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            trail["message"] = "Distributor Successfully Updated"
            trail["data"] =  serializer.data
            return Response(trail, status=status.HTTP_200_OK)
        else:
            trail = serializer.errors
            return Response(trail, status=status.HTTP_403_FORBIDDEN)
        
    # Delet Distributor
    if request.method == 'DELETE':
        try:
            factor = DistributorModel.objects.filter(shop = request.user.shop).get(distributor_id = request.data.get('distributor_id'))
        except:
            raise serializers.ValidationError('Not Found')
        factor.delete()
        trail["message"] = "Distributor Successfully Deleted"
        return Response(trail, status=status.HTTP_200_OK)
        
#########################################################################


#########################################################################
# Distributor List from app
@api_view(['POST', ])
def DistributorListView(request):
    if request.method == 'POST':
        try:
            factors = DistributorModel.objects.filter(shop = request.user.shop)
        except:
            raise serializers.ValidationError('Not Authorized')

        trail = []
        frag = {}
        for i in range(0, len(factors)):

            frag['label'] = str(factors[i].distributor_name) + ' - ' + str(factors[i].company_name)

            frag['distributor_id'] = factors[i].distributor_id
            frag['distributor_name'] = factors[i].distributor_name
            frag['distributor_mobile'] = factors[i].distributor_mobile
            frag['distributor_address'] = factors[i].distributor_address

            trail.append(frag)
            frag = {}
        return Response(trail)
        
#########################################################################


#########################################################################
# Distributor Detail from app [ vendor ]
@api_view(['POST', ])
def DistributorDetailView(request):
    if request.method == 'POST':
        
        try:
            factor = DistributorModel.objects.filter(shop = request.user.shop).get(distributor_id = request.data.get('distributor_id'))
        except:
            raise serializers.ValidationError('Not Found in Function')
        frag = {}

        frag['distributor_id'] = factor.distributor_id
        frag['distributor_name'] = factor.distributor_name
        frag['distributor_mobile'] = factor.distributor_mobile
        frag['distributor_address'] = factor.distributor_address

        return Response(frag)

#########################################################################
##  End Distributor CRUD  ##
#########################################################################




#########################################################################
##  Start Account Activity   ##
#########################################################################
@api_view(['POST'])
def login__mobile(request):
    if request.method == 'POST':
        try:
            try:
                user = Account.objects.get(email=request.data.get("username"))
            except:
                return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            if user:
                if user.check_password(request.data.get("password")):
                    token = Token.objects.get(user=user)
                    return Response({"token": token.key})
                else:
                    return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


        except:
            try:
                user = Account.objects.get(mobile_number=request.data.get("username"))
            except:
                return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            if user:
                if user.check_password(request.data.get("password")):
                    token = Token.objects.get(user=user)
                    return Response({"token": token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)



#########################################################################
@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ResetPasswordView(request):
    account = Account.objects.get(pk=request.user.user_id)
    if request.method == 'POST':
        serializer = ResetPasswordSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save(account=account)
            data = {"Messaage": "Password Updated Successfully", }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors)



#########################################################################
@api_view(['POST', ])
def ForgotPasswordView(request):
    print(request.data.get('email'))
    try:
        account = Account.objects.get(email=request.data.get('email'))
    except :
        data = {"messaage" : "Email not found"}
        return Response(data, status=status.HTTP_403_FORBIDDEN)
        
    if request.method == 'POST':
        forgot_otp = "";
        for i in range(6):
            forgot_otp += str(math.floor(random.random() * 10))
        print(forgot_otp)

        send_mail()
        
        data = {"messaage" : "Password Change Requested",'otp': forgot_otp}
        return Response(data, status=status.HTTP_200_OK)

        
#########################################################################
@api_view(['POST', ])
def ForgotChangePasswordView(request):
    try:
        account = Account.objects.get(email=request.data.get('email'))
    except:
        data = {"messaage" : "Email not found"}
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        serializer = ForgotPasswordSerializer(account , data=request.data)
        if serializer.is_valid():
            serializer.save(account=account)
            data = {"messaage" : "Password Updated Successfully",}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors)



#########################################################################
##  End Account Activity   ##
#########################################################################