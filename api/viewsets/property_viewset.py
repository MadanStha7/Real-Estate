from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from itertools import chain
from datetime import datetime, timezone
from rest_framework import filters
from rest_framework.generics import ListAPIView, GenericAPIView
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
    Locality,
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
    LocalitySerializer,
    # LocationSerializer,
    PropertyCategoriesSerializer,
    PropertyTypeSerializer,
    RentPropertyDetailsSerializer,
    RentalDetailsSerializer,
    PendingPropertySerializer,
    AssignPropertySerializer,
    ResaleDetailsSerializer,
    SellPropertyDetailsSerializer,
    FieldVisitSerializer,
    DashBoardSerialzer,
    PropertyRequestSerializer,
    GallerySerializer,
    PropertyDiscussionSerializer,
    AssignPropertyRequestSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


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


class ListedPropertyViewSet(viewsets.ModelViewSet):
    queryset = BasicDetails.objects.filter(publish=True)
    serializer_class = BasicDetailsSerializer


class PropertyFilter(viewsets.ModelViewSet):
    """
    This views returns property on the basis of filterations.
    """

    queryset = BasicDetails.objects.none()
    serializer_class = BasicDetailsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["property_categories", "property_types", "city"]

    def get_queryset(self):
        verified_property = BasicDetails.objects.filter(publish=True)
        print("verified_property", verified_property)
        property_categories = self.request.query_params.get("property_categories", None)
        property_type = self.request.query_params.get("property_types", None)
        city = self.request.query_params.get("city", None)
        if property_categories:
            queryset = verified_property.filter(
                property_categories__name=property_categories
            )
            return queryset

        if property_type:
            queryset = verified_property.filter(property_types__name=property_type)
            return queryset
        if city:
            queryset = verified_property.filter(city__name=city)
            return queryset
        else:
            return BasicDetails.objects.filter(publish=True)


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


class LocalityViewset(viewsets.ModelViewSet):
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer

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
        if self.action in ["create", "partial_update", "destroy", "approve_property"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]
        if self.action in ["approve_property"]:
            return [IsAuthenticated(), UserIsAdmin()]
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
    Viewsets to store the rent gallery
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


class AssignPropertyViewset(generics.CreateAPIView):
    """Api to assign the property to employee"""

    queryset = BasicDetails.objects.filter(publish=False)
    serializer_class = AssignPropertySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        pending_property = self.request.query_params.get("pending_property_id", False)
        try:
            basic_details = BasicDetails.objects.get(id=pending_property)
        except BasicDetails.DoesNotExist:
            raise ValidationError({"error": "basic details doesn't exist"})
        staff = self.request.data.get("staff")
        due_date = self.request.data.get("due_date")
        description = self.request.data.get("description")
        basic_details.staff = User.objects.get(id=staff)
        basic_details.due_date = due_date
        basic_details.description = description
        basic_details.save()


class FieldVisitViewSet(viewsets.ModelViewSet):
    queryset = FieldVisit.objects.all()
    serializer_class = FieldVisitSerializer
    filterset_fields = ["name", "email", "phone"]


class DashBoardView(APIView):
    def get(self, request, *args, **kwargs):
        listed_property = len(BasicDetails.objects.filter(publish=True))
        sellers = len(BasicDetails.objects.all())
        buyers = len(PropertyRequest.objects.all())
        agents = len(AgentDetail.objects.all())
        property_type_commercial = len(
            BasicDetails.objects.filter(property_types__name="Commercial")
        )
        property_type_residential = len(
            BasicDetails.objects.filter(property_types__name="Residential")
        )
        rental = RentalDetails.objects.filter(basic_details__publish=False)
        resale = ResaleDetails.objects.filter(basic_details__publish=False)

        data = [
            {
                "listed_property": listed_property,
                "sellers": sellers,
                "buyers": buyers,
                "agents": agents,
                "property_type_commercial": property_type_commercial,
                "property_type_residential": property_type_residential,
                "rental": rental,
                "resale": resale,
            }
        ]
        results = DashBoardSerialzer(data, many=True).data
        return Response(results)


class PropertyRequestViewSet(viewsets.ModelViewSet):
    queryset = PropertyRequest.objects.all()
    serializer_class = PropertyRequestSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class PropertyDiscussionViewSet(viewsets.ModelViewSet):
    queryset = PropertyDiscussionBoard.objects.all()
    serializer_class = PropertyDiscussionSerializer

    def get_permissions(self):
        if self.action in ["create", "partial_update", "finish"]:
            return [IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class AssignPropertyRequestViewset(generics.CreateAPIView):
    """Api to assign the propertyrequest to employee"""

    queryset = PropertyRequest.objects.all()
    serializer_class = AssignPropertyRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_request = self.request.query_params.get("property_request_id", False)
        print("property_request")
        try:
            property_request_obj = PropertyRequest.objects.get(id=property_request)
        except BasicDetails.DoesNotExist:
            raise ValidationError({"error": "Property Request doesn't exist"})
        staff = self.request.data.get("staff")
        due_date = self.request.data.get("due_date")
        description_assigned_to_employee = self.request.data.get(
            "description_assigned_to_employee"
        )
        property_request_obj.staff = User.objects.get(id=staff)
        property_request_obj.due_date = due_date
        property_request_obj.description_assigned_to_employee = (
            description_assigned_to_employee
        )
        property_request_obj.save()
