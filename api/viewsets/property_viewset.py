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
    BasicDetailsSerializer,
    CitySerializer,
    PropertyCategoriesSerializer,
    PropertyTypeSerializer, DashBoardSerialzer,
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


class DashBoardView(APIView):
    def get(self, request):
        listed_property = len(BasicDetails.objects.filter(publish=True))
        sellers = len(BasicDetails.objects.all())
        buyers = len(PropertyRequest.objects.all())
        agents = len(AgentDetail.objects.all())
        property_type_commercial = len(PropertyTypes.objects.filter(name="Commercial"))
        property_type_residential = len(PropertyTypes.objects.filter(name="Residential"))
        pending_property = BasicDetails.objects.filter(publish=False)

        data = [
            {
                "listed_property": listed_property,
                "sellers": sellers,
                "buyers": buyers,
                "agents": agents,
                "property_type_commercial": property_type_commercial,
                "property_type_residential": property_type_residential,
                "pending_property": pending_property,
            }
        ]
        results = DashBoardSerialzer(data, many=True).data
        return Response(results)
