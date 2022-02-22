from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

import random,math
from django.core.mail import send_mail
from django.shortcuts import render
from auth_api.models import ForgotTokens, Account
from auth_api.serializers import *
from django.contrib.auth import authenticate

#########################################################################
##  Start Admin CUD  ##
#########################################################################
@api_view(['POST',])
def AdminCudView(request):
    if request.method == 'POST':
        serializer = AdminCreateSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save(user=request.user)
            data['message'] = "Sucessfully Registered"
            data['username'] = account.username

        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)

#########################################################################
##  End Admin CUD  ##
#########################################################################


#########################################################################


#########################################################################
##  Start Visitor CUD  ##
######################################################################### 
@api_view(['POST','PUT'])
def VisitorCudView(request):
    if request.method == 'POST':
        serializer = VisitorCreateSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save(user=request.user)
            data['message'] = "Sucessfully Registered"
            data['username'] = account.username
            token = Token.objects.get(user=account).key

            data['token'] = token
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)

    if request.method == 'PUT':
        visitor = Visitor.objects.get(user=request.user.user_id)
        print(visitor)
        
        serializer = VisitorEditSerializer(visitor, data=request.data)
        trail = {}
        if serializer.is_valid():
            serializer.save()
            trail["message"] = "Successfully Updated"
            trail["Data"] = serializer.data
        return Response(trail, status=status.HTTP_200_OK)

######################################################################### 


######################################################################### 

@api_view(['POST','PUT'])
def VisitorLogin(request):
    if request.method == 'POST':
            data = {}
            try : 
                username = request.POST['email']
                site = request.POST['site']
                user = Visitor.objects.filter(site=site).filter(customer_mobile=username)
                token = Token.objects.get(user=user[0].user).key
                print(user, token)
                # password = request.POST['password']
                # user = authenticate(username=username, password=password)
                data['token'] = token  
                return Response(data, status=status.HTTP_201_CREATED)
            except : 
                print("Inside Creation")
                serializer = VisitorCreateSerializer(data=request.data)
                data={}
                if serializer.is_valid():
                    account = serializer.save(user=request.user)
                    data['message'] = "Sucessfully Registered"
                    data['username'] = account.username
                    token = Token.objects.get(user=account).key

                    data['token'] = token
                else:
                    data = serializer.errors
                return Response(data, status=status.HTTP_201_CREATED)

######################################################################### 


######################################################################### 

@api_view(['POST'])
def VisitorListView(request):
     if request.method == 'POST':
        visitors = Visitor.objects.filter(site=request.data.get('site_id'))
        trail = []
        frag = {}
        for i in range(0, len(visitors)):
            frag['visitor_id'] = visitors[i].visitor_id
            frag['customer_name'] = visitors[i].customer_name
            frag['customer_address'] = visitors[i].customer_address
            frag['customer_mobile'] = visitors[i].customer_mobile
            frag['user'] = visitors[i].user.username
           
            trail.append(frag)
            frag = {}
        return Response(trail)

#########################################################################


#########################################################################

@api_view(['POST'])
def VisitorDetailView(request):
     if request.method == 'POST':
        visitor = Visitor.objects.get(user=request.user.user_id)
        print(visitor)
        frag = {}
        frag['visitor_id'] = visitor.visitor_id
        frag['customer_name'] = visitor.customer_name
        frag['customer_address'] = visitor.customer_address
        frag['customer_mobile'] = visitor.customer_mobile
        frag['user'] = visitor.user.username
           
        return Response(frag)
#########################################################################
##  End Visitor CUD  ##
#########################################################################



#########################################################################


@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ResetPasswordView(request):
    account = Account.objects.get(pk=request.user.user_id)
    if request.method == 'POST':
        serializer = ResetPasswordSerializer(account , data=request.data)
        if serializer.is_valid():
            serializer.save(account=account)
            data = {"messaage" : "Password Updated Successfully",}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors)


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
        forgotToken = ForgotTokens(
            user = account,
            forgot_otp = forgot_otp,
        )
        forgotToken.save()
        send_mail(
            'Forgot Password Code',
            forgotToken.forgot_otp,
            'archtamizh@gmail.com',
            ['vishnuprabhu.bvk@gmail.com'],
            fail_silently=False,
        )
        data = {"messaage" : "Password Change Requested",'otp': forgot_otp}
        return Response(data, status=status.HTTP_200_OK)

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


@api_view(['POST'])
def CheckUsername(request):
    if request.method == 'POST':
        isExist = False
        account = Account.objects.all()
        data = request.data.get('data').lower()
        print(data)
        for i in range(0,len(account)):
            if str(data) == account[i].username:
                isExist = True
            if str(data) == account[i].email:
                isExist = True
        if isExist:
            message = {'message': "taken"}
        else:
            message = {'message': "available"}

        return Response(message)


@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def UserVerificationView(request):
    if request.method == 'POST':
        user=UserModel.objects.get(user=request.user.user_id)
        print(request.data.get('user_otp'))
        if user.user_otp == int(request.data.get('user_otp')):
            user.user_is_active = True
            user.save()
        data={}
        if user.user_is_active:
            data['message'] = "User Verified"
        else:
            data['message'] = "Wrong OTP"
        return Response(data)

