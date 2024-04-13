from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ClubSerializer, UserLoginSerializer, AdministratorSerializer, EventSerializer
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
from .helper1 import check_if_club, check_if_admin



from django.db.models import Q

class AllAdmins(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if check_if_club(request.user):
            admins = Administrator.objects.exclude(role="CO-ORDINATOR")
            serializer = AdministratorSerializer(admins, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        


class Events(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if check_if_club(request.user):
            club = Club.objects.first(user=request.user)
            payload = request.data
            payload["club"] = club.id
            serializer = EventSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
    
    def get(self, request):
        if check_if_club(request.user):
            events = Event.objects.filter(user=request.user)
            ser = EventSerializer(events, many=True).data
            
            return Response(ser, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)




