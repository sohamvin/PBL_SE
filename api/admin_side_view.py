from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ClubSerializer, UserLoginSerializer, AdministratorSerializer, EventSerializer, RequestSerializer
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







