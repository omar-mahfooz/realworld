from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from users.serializers import RegistrationResponseSerializer, UserRegistrationSerializer, UserAuthenticationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ViewSet
import pdb

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data.get('user'))

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                'user': RegistrationResponseSerializer({
                    'email': user.email,
                    'username': user.username,
                    'token': access_token,
                }).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAuthenticationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserAuthenticationSerializer(data=request.data.get('user'))

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    'user': RegistrationResponseSerializer({
                        'email': user.email,
                        'username': user.username,
                        'token': access_token,
                    }).data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ViewSet):
    @action(detail=False, methods=['POST'])
    def registration(self, request):
        user_registration_view = UserRegistrationAPIView.as_view()
        return user_registration_view(request=request)._data
    
    @action(detail=False, methods=['POST'])
    def login(self, request):
        user_authentication_view = UserAuthenticationAPIView.as_view()
        return user_authentication_view(request=request)._data