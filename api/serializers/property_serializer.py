from rest_framework import serializers
from property.models import SocietyAmenities, Property, Gallery, FieldVisit, PropertyDiscussionBoard, PropertyRequest


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocietyAmenities
        fields = ('id', 'title', 'style_class')


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = ('id', 'image', 'video')


class PropertySerializer(serializers.ModelSerializer):
    society_amenities = AmenitiesSerializer(read_only=True, many=True)
    property_type = serializers.CharField(source='get_property_type_display', read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    custom_field = serializers.SerializerMethodField()
    gallery = GallerySerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ('owner', 'property_type', 'owner_name',
                  'agent', 'commercial', 'residential',
                  'apartment', 'apartment_name', 'floor',
                  'storey', 'age', 'listing_type',
                  'membership_plan', 'development_progress_status',
                  'bedroom_hall_kitchen', 'land_area',
                  'build_up_area', 'city', 'address', 'locality',
                  'price', 'condition_type', 'available_for',
                  'expected_rent', 'expected_deposit',
                  'negotiable', 'maintenance', 'available_from',
                  'tenants', 'furnishing', 'parking',
                  'description', 'bedrooms', 'bathrooms',
                  'balcony', 'water_supply', 'non_veg', 'gym',
                  'security', 'viewer', 'secondary_number',
                  'attached_bathroom', 'facing', 'paint',
                  'cleaned', 'available_days', 'start_time',
                  'end_time', 'property_type',
                  'furnished', 'available', 'added_at',
                  'viewed_count', 'updated_at',
                  'society_amenities', 'location', 'latitude',
                  'longitude', 'gallery', 'custom_field'
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

    class Meta:
        model = FieldVisit
        fields = ('id', 'name', 'email', 'phone', 'property_type')


class PropertyDiscussionSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = PropertyDiscussionBoard
        fields = ('id', 'discussion', 'title', 'tags', 'comments', 'property_type')


class PropertyRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyRequest
        fields = ('id', 'name', 'phone', 'email',
                  'request_type', 'property_type',
                  'urgent', 'property_address',
                  'price', 'parking_space',
                  'bedrooms', 'size', 'description')