# # urls.py
from django.urls import path
from .views import UserRegistration, ClubApi, UserLoginView
from .admin_side_view import *
from .club_side_view import *


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('test/', ClubApi.as_view()),
    path('login/', UserLoginView.as_view()),
    path('club/create-event', Events.as_view())
]
