from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from core_api.models import *
# from invoice_api.models import *
from core_api.serializers import *


#########################################################################
##  Start Options CRUD  ##
#########################################################################
# Create Options
@api_view(['POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def OptionsCUDView(request):
    # if request.method == 'POST':
    #     print(request.data)
    #     dupe_optionss_code = OptionsModel.objects.filter(shop=request.user.shop).filter(
    #         options_code=request.data.get('options_code'))
    #     if (len(dupe_optionss_code) >= 1):
    #         return Response({'error': 'Options code already exists'}, status=status.HTTP_403_FORBIDDEN)
    #
    #     serializer = OptionsCreateSerializer(data=request.data)
    #     frag = {}
    #     if serializer.is_valid():
    #         sobject = serializer.save(user=request.user)
    #         frag['message'] = "Options Sucessfully Registered"
    #         frag['options_name'] = sobject.options_name
    #     else:
    #         frag = serializer.errors
    #     return Response(frag, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        try:
            options = BlendingOptionsModel.objects.filter(shop=request.user.shop).get(options_id=request.data.get('options_id'))
        except:
            return Response({'error': 'Options Not Found in Function'}, status=status.HTTP_403_FORBIDDEN)

        serializer = EditOptionsSerializer(options, data=request.data)
        frag = {}
        if serializer.is_valid():
            serializer.save()
            frag["message"] = "Options Successfully Updated"
            frag["data"] = serializer.data
            return Response(frag, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

#########################################################################
