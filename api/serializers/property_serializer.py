from rest_framework import serializers
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
from user.models import UserProfile, AgentDetail

class PropertySerializer(serializers.ModelSerializer):
    """
    return the property details
    """
    class Meta:
        model = PropertyInfo
        fields = (
            "id",
            "property_type",
            "property_adtype",
            "apartment_type",
            "apartment_name",
            "bhk_type",
            "floor",
            "total_floor",
            "age",
            "facing",
            "property_size",
            "owner",
            "agent",
            "staff",
            "location",
            "latitude",
            "longitude",
            "publish",
            "views",
            "listing_type",
            "membership_plan",
            "condition_type",
            "description",
        )


class PropertyListingSerializer(serializers.ModelSerializer):
    """
    return propety listing
    """
    locations=serializers.SlugRelatedField(read_only=True, slug_field="city")
    listing_type= serializers.CharField(source="get_listing_type_display", read_only=True)
    apartment_type= serializers.CharField(source="get_apartment_type_display", read_only=True)
    #gallery=serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    gallery = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='gallery-detail'
    )
    class Meta:
        model=PropertyInfo
        fields = [
            "id",
            "apartment_name",
            "apartment_type",
            "gallery",
            "created_on",
            "locations",
            "listing_type",
        ]
class LocationSerializer(serializers.ModelSerializer):
    """
    Location of property info
    """

    class Meta:
        model = Location
        fields = ("id", "city", "locality", "street", "property_info")


class GallerySerializer(serializers.ModelSerializer):
    """
    gallery of property info
    """
    property_info_value=PropertySerializer(read_only=True)
    class Meta:
        model = Gallery
        fields = ("id", "image", "property_info","property_info_value")


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = (
            "id",
            "bathrooms",
            "balcony",
            "water_supply",
            "gym",
            "non_veg",
            "security",
            "viewer",
            "secondary_number",
            "property_info",
        )


class RentalSerializer(serializers.ModelSerializer):
    """
    Rental
    """

    class Meta:
        model = RentalInfo
        fields = (
            "id",
            "available_for",
            "expected_rent",
            "expected_deposit",
            "negotiable",
            "maintenance",
            "available_from",
            "tenants",
            "furnishing",
            "parking",
            "description",
            "property_info",
        )


class FieldVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldVisit
        fields = ("id", "name", "email", "phone", "property_type")


class PropertyDiscussionSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = PropertyDiscussionBoard
        fields = ("id", "discussion", "title", "tags", "comments", "property_type")


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "id",
            "paint",
            "cleaned",
            "available_days",
            "start_time",
            "end_time",
            "property_type",
        )


class PropertyDetailSerializer(serializers.ModelSerializer):
    """
    this view returns details of property
    """
    #choicefield
    listing_type = serializers.CharField(source="get_listing_type_display")
    
    locations = LocationSerializer(read_only=True)
    rental_info = RentalSerializer(read_only=True, many=True)
    gallery = GallerySerializer(read_only=True, many=True)
    amenities = AmenitiesSerializer(read_only=True, many=True)

    class Meta:
        model = PropertyInfo
        fields = (
            "id",
            "property_type",
            "property_adtype",
            "apartment_type",
            "apartment_name",
            "bhk_type",
            "floor",
            "total_floor",
            "age",
            "facing",
            "property_size",
            "owner",
            "agent",
            "staff",
            "latitude",
            "longitude",
            "publish",
            "locations",
            "rental_info",
            "gallery",
            "amenities",
            "listing_type",
            
        )

