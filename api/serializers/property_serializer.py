from django.db.models.query import QuerySet
from rest_framework import serializers
from property.models import (
    City,
    PropertyCategories,
    PropertyTypes,
    BasicDetails,
    Location,
    RentalDetails,
    Gallery,
    SellPropertyDetails,
    ResaleDetails,
    Amenities,
    FieldVisit,
    PropertyDiscussionBoard,
    PropertyRequest,
    ContactAgent,
    Comment,
    Reply,
)
from .user_serializer import UserProfileSerializer, AdminProfileSerializer
from user.models import (
    UserProfile,
    AgentDetail,
    StaffDetail,
    AdminProfile,
    Notificatons,
)
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import datetime, timezone

User = get_user_model()
