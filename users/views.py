from django.shortcuts import render
from  django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,permissions 
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError as DjangoValidationError
from Serializers import UserSerializers, LoginSerialize
from rest_framework.response import Response
# Create your views here
from django.http import HttpResponse

def newpage(request):
    return  HttpResponse("")


@api_view('POST')
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserSerializers(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user':UserSerializers(user).data,
            'access':str(refresh.access_token),
            'refresh':str(refresh)
        })
    