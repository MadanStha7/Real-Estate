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
    RentPropertyDetails,
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
    RentalDetails,
    LocalityDetails,
)
from api.serializers.property_serializer import (
    AmenitiesSerializer,
    BasicDetailsSerializer,
    CitySerializer,
    LocalityDetailsSerializer,
    # LocationSerializer,
    PropertyCategoriesSerializer,
    PropertyTypeSerializer,
    RentPropertyDetailsSerializer,
    RentalDetailsSerializer,
    GallerySerializer,
    PendingPropertySerializer,
    AssignPropertySerializer,
    ResaleDetailsSerializer,
    SellPropertyDetailsSerializer,
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


class PropertyFilter(viewsets.ModelViewSet):
    """
    This views returns property on the basis of filterations.
    """
    queryset = BasicDetails.objects.all()
    serializer_class = BasicDetailsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["property_categories", "property_type", "city"]

    def get_queryset(self):
        verified_property = BasicDetails.objects.filter(publish=True)
        print(verified_property)
        property_categories = self.request.query_params.get("property_categories", None)
        property_type = self.request.query_params.get("property_type", None)
        city = self.request.query_params.get("city", None)
        if property_categories:
            queryset = verified_property.filter(
                property_categories__name=property_categories)
            return queryset
        if property_type:
            queryset = verified_property.filter(property_type__name=property_type)
            return queryset
        if city:
            queryset = verified_property.filter(city__name=city)
            return queryset
        else:
            pass


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
    """
    Viewsets to store the basic details of both rent and sale
    """

    queryset = BasicDetails.objects.all()
    serializer_class = BasicDetailsSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class RentPropertyDetailsViewset(viewsets.ModelViewSet):
    """
    Viewsets to store the basic details of both rent and sale
    """

    queryset = RentPropertyDetails.objects.all()
    serializer_class = RentPropertyDetailsSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class LocalityDetailsViewset(viewsets.ModelViewSet):
    """
    Viewsets to store the basic details of both rent and sale
    """

    queryset = LocalityDetails.objects.all()
    serializer_class = LocalityDetailsSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class RentalDetailsViewset(viewsets.ModelViewSet):
    """
    Viewsets to store the basic rental details
    """

    queryset = RentalDetails.objects.all()
    serializer_class = RentalDetailsSerializer
    pagination_class = None


class SellPropertyDetailsViewSet(viewsets.ModelViewSet):
    queryset = SellPropertyDetails.objects.all()
    serializer_class = SellPropertyDetailsSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class GalleryViewset(viewsets.ModelViewSet):
    """
    Viewsets to store the gallery
    """

    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    pagination_class = None


class ResaleDetailsViewSet(viewsets.ModelViewSet):
    queryset = ResaleDetails.objects.all()
    serializer_class = ResaleDetailsSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class PendingPropertyViewset(viewsets.ModelViewSet):
    """
    Viewsets to display the pending property
    """

    queryset = BasicDetails.objects.none()
    serializer_class = PendingPropertySerializer
    pagination_class = None

    def get_queryset(self):
        advertisement_type = self.request.query_params.get("advertisement_type", False)
        if advertisement_type == "rent":
            queryset = BasicDetails.objects.filter(
                advertisement_type="R", publish=False
            )
            return queryset
        if advertisement_type == "sale":
            queryset = BasicDetails.objects.filter(
                advertisement_type="S", publish=False
            )
            return queryset
        else:
            queryset = BasicDetails.objects.filter(publish=False)
            return queryset


class AmenitiesViewSet(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=["GET"])
    def approve_property(self, request):
        property = self.request.query_params.get("property_id", None)
        if property:
            get_property = BasicDetails.objects.get(id=property)
            get_property.publish = True
            get_property.save()
            return Response(
                {"message": "property successfully approved"}, status=status.HTTP_200_OK
            )

        else:
            raise ValidationError({"error": "property is required"})


class AssignPropertyViewset(generics.UpdateAPIView):
    """Api to assign the property to employee"""

    queryset = BasicDetails.objects.filter(publish=False)
    serializer_class = AssignPropertySerializer
    permission_classes = [IsAuthenticated]
