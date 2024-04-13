from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ClubSerializer, UserLoginSerializer
from .models import Club, Administrator, Request, ReviewMessage, Event
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status    
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import timedelta, datetime
from rest_framework.authentication import TokenAuthentication

class ClubApi(APIView):
    def get(self, request):
        club1 = Club.objects.get(id=1)

        serializer = ClubSerializer(club1)

        return Response(serializer.data)

class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
    
class UserLoginView(APIView):
    def post(self, request):

        ser = UserLoginSerializer(data=request.data)
        if ser.is_valid():
            username = ser.validated_data['username']
            password = ser.validated_data['password']
            user = authenticate(username=username, password=password, request=request)
            if user is not None:
                token_obj, _ = Token.objects.get_or_create(user=user)
                response = Response({'message': 'Login successful', 'token': str(token_obj)}, status=status.HTTP_200_OK)
                response['Authorization'] = 'Token ' + str(token_obj)
                return response
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)




# class 


# Create your views here.
