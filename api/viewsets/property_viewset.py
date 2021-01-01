from django.db.models import Q
from rest_framework import viewsets
from property.models import SocietyAmenities, Property, PropertyGallery, FieldVisit, PropertyDiscussionBoard
from api.serializers.property_serializer import PropertySerializer, AmenitiesSerializer, PropertyGallerySerializer, \
    FieldVisitSerializer, PropertyDiscussionSerializer


class AmenitiesViewSet(viewsets.ModelViewSet):

    queryset = SocietyAmenities.objects.all()
    serializer_class = AmenitiesSerializer


class PropertyViewSet(viewsets.ModelViewSet):

    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filterset_fields = ['bedrooms', 'storey' , 'membership_plan']

    def get_queryset(self):
        # params = self.request.query_params
        # bedrooms = params.get("bedrooms")
        # if bedrooms:
        #     self.queryset = self.queryset.filter(bedrooms=bedrooms)
        if self.request.user and not self.request.user.is_superuser:
            self.queryset = self.queryset.filter(
                Q(owner=self.request.user) | Q(agent=self.request.user))
        return self.queryset


class PropertyGalleryViewSet(viewsets.ModelViewSet):

    queryset = PropertyGallery.objects.all()
    serializer_class = PropertyGallerySerializer


class FieldVisitViewSet(viewsets.ModelViewSet):

    queryset = FieldVisit.objects.all()
    serializer_class = FieldVisitSerializer


class PropertyDiscussionViewSet(viewsets.ModelViewSet):

    queryset = PropertyDiscussionBoard.objects.all()
    serializer_class = PropertyDiscussionSerializer
