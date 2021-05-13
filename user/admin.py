from django.contrib import admin
from user.models import AgentDetail, UserProfile, StaffDetail, Contact, AdminProfile

# Register your models here.
admin.site.register([AgentDetail, UserProfile, StaffDetail, AdminProfile, Contact])
