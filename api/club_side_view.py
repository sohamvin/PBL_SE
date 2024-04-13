from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ClubSerializer, UserLoginSerializer, AdministratorSerializer, EventSerializer, RequestSerializer, RequestMapSerializer
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
from .helper1 import check_if_club, check_if_admin, getAdmin, getClub
from rest_framework.exceptions import NotFound


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
            club = getClub(request.user)
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
            club = getClub(request.user)
            events = Event.objects.filter(club=club)
            ser = EventSerializer(events, many=True).data
            
            return Response(ser, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        

class Requests(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if check_if_club(request.user):
            payload = request.data
            club = getClub(request.user)
            payload["club"] = club.id
            serializer = RequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
    def put(self, request, pk):
        #will use same for administartor part
            if check_if_club(request.user):
                try:
                    request_instance = Request.objects.get(pk=pk)
                    
                    # Update only the specified fields if they are provided in the request data
                    # fields_to_update = ['final_approve_date', 'status', 'body']
                    fields_to_update = ['body']
                    for field in fields_to_update:
                        if field in request.data:
                            setattr(request_instance, field, request.data[field])
                    
                    request_instance.save()
                    
                    # Serialize the updated instance and return the response
                    serializer = RequestSerializer(request_instance)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Request.DoesNotExist:
                    # Return custom error response
                    return Response({"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)  
            else:
                return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
    def get(self, request, pk):
        #where pk is event id
        if check_if_club(request.user):
            try:
                event = Event.objects.get(pk=pk)
                
                requests = Request.objects.filter(event=event)
                
                ser = RequestSerializer(requests, many=True).data
                
                return Response(ser, status=status.HTTP_200_OK)
                
            except Event.DoesNotExist:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)  
        else:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        


class SendRequest(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if check_if_club(request.user):
            ser = RequestMapSerializer(data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_201_CREATED)
            return Response(ser.error_messages, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

    


# {
#     "request_id": "12345678",
#     "club": 1,  // Assuming the club ID is 1
#     "event": 1,  // Assuming the event ID is 1
#     "title": "Sample Request",
#     "body": "This is a sample request body.",
#     "date": "2024-04-14",  // Date format: YYYY-MM-DD
#     "final_approve_date": null,  // If not applicable, you can send null or omit this field
#     "subject": "Sample Subject",
#     "status": "PENDING"  // Assuming the status is PENDING
# }

    




