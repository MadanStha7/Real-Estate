from rest_framework import serializers
from property.models import Property, Gallery, FieldVisit, PropertyDiscussionBoard, PropertyRequest, CityCategory, ListingCategory


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = ('id', 'image', 'video')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityCategory
        fields = ('name')


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingCategory
        fields = ('name')


class PropertySerializer(serializers.ModelSerializer):
    #property_type = serializers.CharField(source='get_property_type_display', read_only=True)
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    custom_field = serializers.SerializerMethodField()
    gallery = GallerySerializer(many=True, read_only=True)
    city = CitySerializer(many=True, read_only=True)
    listing = ListingSerializer(many=True)

    class Meta:
        model = Property
        fields = ('owner_name', 'agent', 'staff',
                  'commercial', 'residential',
                  'apartment', 'apartment_name', 'bhk_type', 'floor',
                  'total_floor', 'age', 'facing', 'property_size',
                  'listing',
                  'city', 'address', 'locality',
                  'available_for',
                  'expected_rent', 'expected_deposit',
                  'negotiable', 'maintenance', 'available_from',
                  'preferred_tenants', 'furnishing', 'parking',
                  'description', 'gallery', 'membership_plan', 'development_progress_status',
                  'build_up_area', 'uid', 'price', 'condition_type',
                  'bedrooms', 'bathrooms', 'balcony',
                  'water_supply', 'gym', 'non_veg',
                  'gated_security', 'viewer', 'secondary_number',
                  'paint', 'cleaned',
                  'available_days', 'start_time', 'end_time',
                  'available', 'added_at',
                  'viewed_count', 'updated_at', 'location',
                  'latitude', 'longitude', 'custom_field'
                  )

    def get_custom_field(self, obj):
        return dict(a=1, b=3, uid=obj.uid)


class PropertyDetailSerializer(serializers.ModelSerializer):
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
