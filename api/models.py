from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils import timezone
import uuid
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
import random
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from enum import Enum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import random


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractUser):
#     team_id = models.CharField(max_length=256, primary_key=True)
#     email = models.EmailField(unique=True)
#     # username = models.CharField(max_length=256, unique=True) # overrided , but must be team name , not username of user


#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     def save(self, *args, **kwargs):
#         if not self.team_id:
#             self.team_id = str(uuid.uuid4())
#         super().save(*args, **kwargs)

class ROLE(Enum):
    HOD_ENTC = 'HOD_ENTC'
    HOD_CE = 'HOD_CE'
    HOD_IT = 'HOD_IT'
    PRINCIPAL = 'PRINCIPAL'
    DIRECTOR = 'DIRECTOR'
    CO_ORDINATOR = 'CO-ORDINATOR'
    PE_TEACHER = 'PE_TEACHER'

class STATUS(Enum):
    PENDING = 'PENDING'
    UNDER_REVIEW = 'UNDER_REVIEW'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

class Club(models.Model):
    name = models.CharField(_("Club Name"), max_length=255)
    club_url = models.URLField(_("Club Logo URL"), max_length=200, null=False, blank=False)
    club_head = models.CharField(_("Club Head"), max_length=50, blank=True)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Club")
        verbose_name_plural = _("Clubs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Club_detail", kwargs={"pk": self.pk})


class Administrator(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    role = models.CharField(_("Role"), max_length=50, choices=[(role.value, role.value) for role in ROLE])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)
    # if administartor type is CO-ORDINATOR, of which club? so this field is for that. 

    class Meta:
        verbose_name = _("Administrator")
        verbose_name_plural = _("Administrators")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Administrator_detail", kwargs={"pk": self.pk})

class Event(models.Model):
    name = models.CharField(_("Event Name"), max_length=50)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.TextField()
    request_id = models.CharField(_("ID"), max_length=8, primary_key=True, default='00000000')
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Event_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.request_id or self.request_id == '00000000':
            unique_id = str(random.randint(10000000, 99999999))
            while Event.objects.filter(request_id=unique_id).exists():
                unique_id = str(random.randint(10000000, 99999999))
            self.request_id = unique_id
        super().save(*args, **kwargs)
    




class Request(models.Model):
    request_id = models.CharField(_("ID"), max_length=8, primary_key=True, default='00000000')
    club = models.ForeignKey(Club, verbose_name=_("Club"), on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name=_("Event"), on_delete=models.CASCADE, null=True)
    title = models.CharField(_("Title"), max_length=250)
    body = models.TextField(_("Body"))
    date = models.DateField(_("Date"), auto_now_add=True)
    final_aprove_date = models.DateField(null=True)
    subject = models.TextField(_("Subject"))
    status = models.CharField(_("Status"), max_length=50, choices=[(status.value, status.value) for status in STATUS], default=STATUS.PENDING.value)

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Request_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.request_id or self.request_id == '00000000':
            unique_id = str(random.randint(10000000, 99999999))
            while Event.objects.filter(request_id=unique_id).exists():
                unique_id = str(random.randint(10000000, 99999999))
            self.request_id = unique_id
        super().save(*args, **kwargs)

class ReviewMessage(models.Model):
    message = models.TextField(_("Message"))
    request = models.ForeignKey(Request, verbose_name=_("Request"), on_delete=models.CASCADE)
    administrator = models.ForeignKey(Administrator, verbose_name=_("Administrator"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Review Message")
        verbose_name_plural = _("Review Messages")

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse("ReviewMessage_detail", kwargs={"pk": self.pk})
    




# each injstance of this is sending to each administartor
class RequestMap(models.Model):
    request = models.ForeignKey(Request, verbose_name=_(""), on_delete=models.CASCADE)
    sendto = models.ForeignKey(Administrator, verbose_name=_(""), on_delete=models.CASCADE)
    status = models.CharField(_("Status"), max_length=50, choices=[(status.value, status.value) for status in STATUS], default=STATUS.PENDING.value)
    

    class Meta:
        verbose_name = _("RequestMap")
        verbose_name_plural = _("RequestMaps")

    def get_absolute_url(self):
        return reverse("RequestMap_detail", kwargs={"pk": self.pk})
