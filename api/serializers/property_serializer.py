from rest_framework import serializers
from property.models import SocietyAmenities, Property, PropertyGallery, FieldVisit, PropertyDiscussionBoard


class AmenitiesSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = SocietyAmenities
        fields = ['id', 'title', 'style_class', ]


class PropertySerializer(serializers.ModelSerializer):
    society_amenities = AmenitiesSerializer(read_only=True, many=True)
    property_type = serializers.CharField(source='get_property_type_display')
    owner_name = serializers.CharField(source='owner.username')
    custom_field = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ("society_amenities", "owner", "bedrooms",
                  "price", "address", "build_up_area",
                  "viewed_count", "added_at", "property_type",
                  "owner_name", "custom_field", "storey")

    def get_custom_field(self, obj):
        return dict(a=1, b=3, uid=obj.uid)


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
