from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from itertools import chain
import django_filters.rest_framework
from rest_framework import filters
from rest_framework.response import Response

from property.models import (
    PropertyInfo,
    Gallery,
    FieldVisit,
    PropertyDiscussionBoard,
    RentalInfo,
    Amenities,
    Schedule,
    Location,
)
from api.serializers.property_serializer import (
    PropertySerializer,
    FieldVisitSerializer,
    PropertyDiscussionSerializer,
    RentalSerializer,
    GallerySerializer,
    AmenitiesSerializer,
    ScheduleSerializer,
    LocationSerializer,
    PropertyDetailSerializer,
    PropertyListingSerializer,
)


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = PropertyInfo.objects.all()
    serializer_class = PropertySerializer
    # filter_fields = ['bedrooms', 'storey', 'membership_plan', 'listing_type']

    # def get_queryset(self):
    #     # params = self.request.query_params
    #     # bedrooms = params.get("bedrooms")
    #     # if bedrooms:
    #     #     self.queryset = self.queryset.filter(bedrooms=bedrooms)
    #     queryset = self.queryset
    #     if self.request.user.is_authenticated:
    #         if self.request.user and not self.request.user.is_superuser:
    #             queryset = self.queryset.filter(
    #                 Q(owner=self.request.user) | Q(agent=self.request.user)
    #             )
    #     return queryset

    # """def get_queryset(self):

    #     assert self.queryset is not None, (
    #             "'%s' should either include a `queryset` attribute, "
    #             "or override the `get_queryset()` method."
    #             % self.__class__.__name__
    #     )
    # """

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = PropertySerializer(instance)
    #     # amenities = []
    #     field_visits = []
    #     discussion = []
    #     params = self.request.query_params
    #     tab = params.get("tab")
    #     if tab == "amenities":
    #         amenities = AmenitiesSerializer(
    #             instance.society_amenities.all(), many=True
    #         ).data
    #     elif tab == "field_visit":
    #         field_visits = FieldVisitSerializer(instance.image.all(), many=True).data
    #     elif tab == "discussion":
    #         discussion = PropertyDiscussionSerializer(
    #             instance.discussion.all(), many=True
    #         ).data
    #     return Response(
    #         dict(
    #             data=serializer.data,
    #             amenities=amenities,
    #             field_visits=field_visits,
    #             discussion=discussion,
    #         )
    #     )


class PropertyList(generics.ListAPIView):
    """
    This views returns listing of porperty in homepage
    """

    serializer_class = PropertyDetailSerializer
    queryset = PropertyInfo.objects.filter(publish=True)


class PropertyTop(generics.ListAPIView):
    """
    This views returns listing of top listing property
    """

    serializer_class = PropertyListingSerializer

    def get_queryset(self):
        top_category = PropertyInfo.objects.filter(
            listing_type="T",
        ).filter(publish=True)
        # premium_category = PropertyInfo.objects.filter(listing_type="P").filter(
        #     publish=True
        # )
        # featured_category = PropertyInfo.objects.filter(listing_type="F").filter(
        #     publish=True
        # )
        return top_category


class PropertyPremium(generics.ListAPIView):
    """
    This views returns listing of premium property
    """

    serializer_class = PropertyListingSerializer

    def get_queryset(self):
        premium_category = PropertyInfo.objects.filter(listing_type="P").filter(
            publish=True
        )
        return premium_category

class PropertyFeatured(generics.ListAPIView):
    """
    This views returns featured property
    """

    serializer_class = PropertyListingSerializer

    def get_queryset(self):
        featured_category = PropertyInfo.objects.filter(listing_type="F").filter(
            publish=True
        )
        return featured_category




class RentalViewSet(viewsets.ModelViewSet):
    queryset = RentalInfo.objects.all()
    serializer_class = RentalSerializer
    filterset_fields = ["available_for", "tenants", "parking"]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class AmentitesViewSet(viewsets.ModelViewSet):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer
    # fieldset_fields=["bathrooms","balcony","gym"]


class FieldVisitViewSet(viewsets.ModelViewSet):
    queryset = FieldVisit.objects.all()
    serializer_class = FieldVisitSerializer
    filterset_fields = ["name", "email", "phone"]


class PropertyDiscussionViewSet(viewsets.ModelViewSet):
    queryset = PropertyDiscussionBoard.objects.all()
    serializer_class = PropertyDiscussionSerializer
    filterset_fields = ["discussion"]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class ScheduleList(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = ScheduleSerializer(queryset, many=True)
        return Response(serializer.data)


class PropertyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyInfo.objects.all()
    serializer_class = PropertyDetailSerializer

