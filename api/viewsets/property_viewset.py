from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from itertools import chain
from datetime import datetime, timezone
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from user.models import AgentDetail, UserProfile, AdminProfile
from django.contrib.auth.models import Group
from api.permissions.user_permission import (
    UserIsAuthenticated,
    UserIsAdmin,
    UserIsStaffDetail,
    UserIsBuyerOrSeller,
    UserIsAgentDetail,
)
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
from api.serializers.property_serializer import (
    AmenitiesSerializer,
    BasicDetailsSerializer,
    CitySerializer,
    PropertyCategoriesSerializer,
    PropertyTypeSerializer,
    ResaleDetailsSerializer,
    SellPropertyDetailsSerializer
)

"""===================================
-- Property model on client side starts ---
======================================"""


class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class PropertyTypesViewSet(viewsets.ModelViewSet):
    queryset = PropertyTypes.objects.all()
    serializer_class = PropertyTypeSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class PropertyCategoryViewset(viewsets.ModelViewSet):
    queryset = PropertyCategories.objects.all()
    serializer_class = PropertyCategoriesSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class BasicDetailsViewset(viewsets.ModelViewSet):
    queryset = BasicDetails.objects.all()
    serializer_class = BasicDetailsSerializer
    pagination_class = None


class SellPropertyDetailsViewSet(viewsets.ModelViewSet):
    queryset = SellPropertyDetails.objects.all()
    serializer_class = SellPropertyDetailsSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class ResaleDetailsViewSet(viewsets.ModelViewSet):
    queryset = ResaleDetails.objects.all()
    serializer_class = ResaleDetailsSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class AmenitiesViewSet(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]
