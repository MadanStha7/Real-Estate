from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response
from property.models import \
    (SocietyAmenities, Property, PropertyGallery,
     FieldVisit, PropertyDiscussionBoard)
from api.serializers.property_serializer import \
    (PropertySerializer, AmenitiesSerializer, PropertyGallerySerializer,
     FieldVisitSerializer, PropertyDiscussionSerializer, PropertyDetailSerializer)


class AmenitiesViewSet(viewsets.ModelViewSet):
    queryset = SocietyAmenities.objects.all()
    serializer_class = AmenitiesSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filterset_fields = ['bedrooms', 'storey', 'membership_plan', 'listing_type']
    """
    def get_queryset(self):
        # params = self.request.query_params
        # bedrooms = params.get("bedrooms")
        # if bedrooms:
        #     self.queryset = self.queryset.filter(bedrooms=bedrooms)
        if self.request.user and not self.request.user.is_superuser:
            self.queryset = self.queryset.filter(
                Q(owner=self.request.user) | Q(agent=self.request.user))
        return self.queryset
    """

    def get_queryset(self):

        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PropertySerializer(instance)
        amenities = []
        field_visits = []
        discussion = []
        params = self.request.query_params
        tab = params.get("tab")
        if tab == "amenities":
            amenities = AmenitiesSerializer(instance.society_amenities.all(), many=True).data
        elif tab == "field_visit":
            field_visits = FieldVisitSerializer(instance.image.all(), many=True).data
        elif tab == "discussion":
            discussion = PropertyDiscussionSerializer(instance.discussion.all(), many=True).data
        return Response(
            dict(data=serializer.data,
                 amenities=amenities, field_visits=field_visits,
                 discussion=discussion))


class PropertyGalleryViewSet(viewsets.ModelViewSet):
    queryset = PropertyGallery.objects.all()
    serializer_class = PropertyGallerySerializer


class FieldVisitViewSet(viewsets.ModelViewSet):
    queryset = FieldVisit.objects.all()
    serializer_class = FieldVisitSerializer
    filterset_fields = ['name', 'email', 'phone']


class PropertyDiscussionViewSet(viewsets.ModelViewSet):
    queryset = PropertyDiscussionBoard.objects.all()
    serializer_class = PropertyDiscussionSerializer
    filterset_fields = ['discussion']
