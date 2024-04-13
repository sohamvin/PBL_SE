from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ClubSerializer, UserLoginSerializer, AdministratorSerializer, EventSerializer, RequestSerializer, RequestMapSerializer
from .models import Club, Administrator, Request, ReviewMessage, Event, RequestMap, STATUS
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
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import logging
class ShowRequests(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if check_if_admin(request.user):
            admin = getAdmin(request.user)
            # Fetch RequestMap instances associated with the authenticated user
            request_maps = RequestMap.objects.filter(sendto=admin)
                        
            # Extract request_ids from RequestMap instances
            request_ids = request_maps.values_list('request_id', flat=True)
            
            # Fetch all related Request instances using a single query
            requests = Request.objects.filter(request_id__in=request_ids)
            
            # Serialize the Request instances
            serializer = RequestSerializer(requests, many=True, context={'request': request}).data
            
            for ele in serializer:
                club = Club.objects.get(id=ele["club"])
                club_ser = ClubSerializer(club).data
                ele["club_data"] = club_ser
            
            return Response(serializer, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
        



logger = logging.getLogger(__name__)

class ReviewRequests(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        if not check_if_admin(request.user):
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

        try:
            request_instance = Request.objects.get(pk=pk)
            event = request_instance.event
            admin = getAdmin(request.user)
            maps = RequestMap.objects.filter(request=request_instance, sendto=admin).first()
            
            if not maps:
                return Response({"message": "Request wasn't sent to you"}, status=status.HTTP_404_NOT_FOUND)
            
            new_status = request.data.get("status")
            maps.status = new_status
            maps.save()

            all_maps = RequestMap.objects.filter(request=request_instance)
            all_approved = all(m.status == "APPROVED" for m in all_maps)

            if all_approved:
                request_instance.status = "APPROVED"
                request_instance.save()

            serializer = RequestSerializer(request_instance)
            event_serializer = EventSerializer(event)
            response_data = serializer.data
            response_data["event_name"] = event_serializer.data["name"]

            return Response(response_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("Request not found with id: %s", pk)
            return Response({"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("An error occurred: %s", str(e))
            return Response({"error": "An error occurred while processing your request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)