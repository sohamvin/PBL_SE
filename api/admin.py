from django.contrib import admin
from .models import Administrator, Club, Event

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'club_head', 'user']

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ['name', 'role']
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display= ['name']

# Register your models here.
