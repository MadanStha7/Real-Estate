from rest_framework import serializers
from property.models import SocietyAmenities, Property, PropertyGallery, FieldVisit, PropertyDiscussionBoard


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocietyAmenities
        fields = ['id', 'title', 'style_class']


class PropertyGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyGallery
        fields = ['id', 'image', 'property']


class PropertySerializer(serializers.ModelSerializer):
    # society_amenities = AmenitiesSerializer(read_only=True, many=True)
    # property_type = serializers.CharField(source='get_property_type_display')
    # owner_name = serializers.CharField(source='owner.username')
    # custom_field = serializers.SerializerMethodField()
    # gallery = PropertyGallerySerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ('owner', "agent",
                  'membership_plan', 'development_progress_status',
                  'bedroom_hall_kitchen', 'land_area',
                  'build_up_area', 'address',
                  'price', 'condition_type', 'bedrooms',
                  'bathrooms', 'available_from', 'city',
                  'available_for', 'storey', 'parking',
                  'attached_bathroom', 'facing', 'property_type',
                  'furnished', 'available', 'added_at',
                  'viewed_count', 'updated_at', 'description',
                  'location', 'latitude',
                  'longitude'
                  )

    def get_custom_field(self, obj):
        return dict(a=1, b=3, uid=obj.uid)


class PropertyDetailSerializer(serializers.ModelSerializer):
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


class FieldVisitSerializer(serializers.ModelSerializer):
    # property = serializers.RelatedField(source='property', read_only=True)

    class Meta:
        model = FieldVisit
        fields = ['id', 'name', 'email', 'phone', 'property']


class PropertyDiscussionSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    # property = serializers.RelatedField(source='property', read_only=True)

    class Meta:
        model = PropertyDiscussionBoard
        fields = ['id', 'discussion', 'title', 'tags', 'comments', 'property']
