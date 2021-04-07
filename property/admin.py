from django.contrib import admin
from django.apps import apps

from .models import *
# Register your models here.

admin.site.register([PropertyInfo,Location,RentalInfo,Gallery,Amenities,FieldVisit,PropertyDiscussionBoard,Schedule])
