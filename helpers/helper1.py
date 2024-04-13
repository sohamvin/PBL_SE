from ..api.models import Club, Administrator, Event


def check_if_admin(user):
    admin_exists = Administrator.objects.first(user=user)
    if not admin_exists:
        return False
    else:
        return True
    

def check_if_club(user):
    club_exists = Club.objects.first(user=user)
    
    if not club_exists:
        return False
    else:
        return True