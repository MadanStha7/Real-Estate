from django.contrib import admin
from django.apps import apps

from .models import (
    City,
    PropertyCategories,
    PropertyTypes,
    BasicDetails,
    LocalityDetails,
    RentalDetails,
    RentGallery,
    SellPropertyDetails,
    ResaleDetails,
    Amenities,
    FieldVisit,
    PropertyDiscussionBoard,
    PropertyRequest,
    ContactAgent,
    Comment,
    Reply,
    Locality,
)

# Register your models here.

admin.site.register(
    [
        City,
        PropertyCategories,
        PropertyTypes,
        BasicDetails,
        LocalityDetails,
        RentalDetails,
        RentGallery,
        SellPropertyDetails,
        ResaleDetails,
        Amenities,
        FieldVisit,
        PropertyDiscussionBoard,
        PropertyRequest,
        ContactAgent,
        Comment,
        Reply,
        Locality,
    ]
)
