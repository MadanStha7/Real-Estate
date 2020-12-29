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


class PropertyGalleryViewSet(viewsets.ModelViewSet):

    queryset = PropertyGallery.objects.all()
    serializer_class = PropertyGallerySerializer


class FieldVisitViewSet(viewsets.ModelViewSet):

    queryset = FieldVisit.objects.all()
    serializer_class = FieldVisitSerializer


class PropertyDiscussionViewSet(viewsets.ModelViewSet):

    queryset = PropertyDiscussionBoard.objects.all()
    serializer_class = PropertyDiscussionSerializer
