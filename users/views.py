from django.shortcuts import render
from  django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,permissions 
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError as DjangoValidationError
from .Serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
# Create your views here
from django.http import HttpResponse
from .models import User

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializers = UserSerializer(data=request.data)
    if serializers.is_valid():
        user = serializers.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            return Response({'detail':"this user does not exist"},status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(
            username = user.username,
            password = serializer.validated_data['password']

        )

        if user:
            refresh  = RefreshToken.for_user(user).data
            return Response ({
                "user": UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)


            })
        return Response({'detail':"invalid credentials"})
    return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    