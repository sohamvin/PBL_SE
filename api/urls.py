# # urls.py
from django.urls import path
from .views import UserRegistration, ClubApi, UserLoginView

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('test/', ClubApi.as_view()),
    path('login/', UserLoginView.as_view()),
]
