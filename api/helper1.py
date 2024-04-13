from .models import Club, Administrator
from django.contrib.auth.models import User


def check_if_admin(user):
    admin_exists = Administrator.objects.filter(user=user).exists()
    return admin_exists
    

from .models import Club

def check_if_club(user):
    club_exists = Club.objects.filter(user=user).exists()
    return club_exists
