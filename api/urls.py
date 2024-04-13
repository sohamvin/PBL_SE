# # urls.py
from django.urls import path
from .views import UserRegistration, ClubApi, UserLoginView
from .admin_side_view import *
from .club_side_view import *


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('test/', ClubApi.as_view()),
    path('login/', UserLoginView.as_view()),
    path('club/event', Events.as_view()),
    path("club/request", Requests.as_view()),
    path("club/request/<int:pk>", Requests.as_view()),
    path("club/admins", AllAdmins.as_view()),
    path("club/send", SendRequest.as_view()),
    path("admin/requests", ShowRequests.as_view()),
    path("admin/requests/<str:pk>", ReviewRequests.as_view()),
]
