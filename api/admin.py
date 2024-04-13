from django.contrib import admin
from .models import Administrator, Club, Event, RequestMap, Request

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'club_head', 'user']

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ['name', 'role']
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display= ['name']
    
@admin.register(RequestMap)
class Radmin(admin.ModelAdmin):
    list_display = ['status']

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'subject', 'status']

    # def display_id(self, obj):
    #     return str(obj.id)
    # display_id.short_description = 'ID'


# Register your models here.
