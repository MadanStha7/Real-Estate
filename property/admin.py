from django.contrib import admin
from django.apps import apps

from .models import (
    City,
    PropertyInfo,
    Location,
    RentalInfo,
    Gallery,
    Amenities,
    FieldVisit,
    PropertyDiscussionBoard,
    Schedule,
    ContactAgent
)

# Register your models here.

admin.site.register(
    [
        City,
        PropertyInfo,
        Location,
        RentalInfo,
        Gallery,
        Amenities,
        FieldVisit,
        PropertyDiscussionBoard,
        Schedule,
        ContactAgent
    ]
)
