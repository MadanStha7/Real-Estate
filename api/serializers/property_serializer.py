from rest_framework import serializers
from property.models import SocietyAmenities, Property, PropertyGallery, FieldVisit, PropertyDiscussionBoard


class AmenitiesSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = SocietyAmenities
        fields = ['id', 'title', 'style_class']


class PropertySerializer(serializers.ModelSerializer):
    society_amenities = AmenitiesSerializer(read_only=True, many=True)

    class Meta:
        model = Property
        fields = ['__all__']


class PropertyGallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyGallery
        fields = ['id', 'image', 'property']


class FieldVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldVisit
        fields = ['id', 'name', 'email', 'phone', 'property']


class PropertyDiscussionSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = PropertyDiscussionBoard
        fields = ['id', 'discussion', 'title', 'tags', 'comments', 'property']
