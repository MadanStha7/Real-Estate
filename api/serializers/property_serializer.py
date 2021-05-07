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
    City,
    PropertyRequest,
)
from user.models import UserProfile, AgentDetail


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")


class PropertySerializer(serializers.ModelSerializer):
    """
    return the property details in homepage
    """

    listing_type = serializers.CharField(required=False)
    membership_plan = serializers.CharField(required=False)
    condition_type = serializers.CharField(required=False)
    created_on = serializers.CharField(read_only=True)

    class Meta:
        model = PropertyInfo
        fields = (
            "id",
            "city",
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
            "price",
            "created_on"
        )


class PropertyListingSerializer(serializers.ModelSerializer):
    """
    return property listing
    """

    locations = serializers.SlugRelatedField(read_only=True, slug_field="city")
    listing_type = serializers.CharField(
        source="get_listing_type_display", read_only=True
    )
    apartment_type = serializers.CharField(
        source="get_apartment_type_display", read_only=True
    )
    gallery = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="gallery-detail"
    )
    created_on = serializers.CharField(read_only=True)

    class Meta:
        model = PropertyInfo
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

    city = CitySerializer(read_only=True)

    class Meta:
        model = Location
        fields = ("id", "city", "locality", "street", "property_info")


class GallerySerializer(serializers.ModelSerializer):
    """
    gallery of property info
    """

    property_info_value = PropertySerializer(read_only=True)

    class Meta:
        model = Gallery
        fields = ("id", "image", "property_info", "property_info_value")


class AmenitiesSerializer(serializers.ModelSerializer):
    balcony_value = serializers.CharField(source="get_balcony_display", read_only=True)
    water_supply_value = serializers.CharField(
        source="get_water_supply_display", read_only=True
    )

    gym_value = serializers.CharField(source="get_gym_display", read_only=True)
    non_veg_value = serializers.CharField(source="get_non_veg_display", read_only=True)
    security_value = serializers.CharField(
        source="get_security_display", read_only=True
    )
    viewer_value = serializers.CharField(source="get_viewer_display", read_only=True)

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
            "balcony_value",
            "water_supply_value",
            "gym_value",
            "non_veg_value",
            "security_value",
            "viewer_value",
            "property_info",
        )


class RentalSerializer(serializers.ModelSerializer):
    """
    Rental
    """

    available_for_value = serializers.CharField(
        source="get_available_for_display", read_only=True
    )
    maintenance_value = serializers.CharField(
        source="get_maintenance_display", read_only=True
    )

    tenants_value = serializers.CharField(source="get_tenants_display", read_only=True)
    furnishing_value = serializers.CharField(
        source="get_furnishing_display", read_only=True
    )
    parking_value = serializers.CharField(source="get_parking_display", read_only=True)

    class Meta:
        model = RentalInfo
        fields = (
            "id",
            "available_for_value",
            "available_for",
            "expected_rent",
            "expected_deposit",
            "negotiable",
            "maintenance",
            "maintenance_value",
            "available_for_value",
            "available_from",
            "tenants",
            "tenants_value",
            "furnishing",
            "furnishing_value",
            "parking_value",
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
    paint_value = serializers.CharField(source="get_paint_display", read_only=True)
    cleaned_value = serializers.CharField(source="get_cleaned_display", read_only=True)
    available_days_value = serializers.CharField(
        source="get_available_days_display", read_only=True
    )

    class Meta:
        model = Schedule
        fields = (
            "id",
            "paint",
            "paint_value",
            "cleaned",
            "cleaned_value",
            "available_days",
            "available_days_value",
            "start_time",
            "end_time",
            "property_type",
        )


class PropertyDetailSerializer(serializers.ModelSerializer):
    """
    this view returns details of property
    """

    # choicefield for property
    listing_type = serializers.CharField(source="get_listing_type_display")
    property_type = serializers.CharField(source="get_property_type_display")
    property_adtype = serializers.CharField(source="get_property_adtype_display")
    apartment_type = serializers.CharField(source="get_apartment_type_display")
    bhk_type = serializers.CharField(source="get_bhk_type_display")
    floor = serializers.CharField(source="get_floor_display")
    total_floor = serializers.CharField(source="get_total_floor_display")
    age = serializers.CharField(source="get_age_display")
    facing = serializers.CharField(source="get_facing_display")
    membership_plan = serializers.CharField(source="get_membership_plan_display")
    condition_type = serializers.CharField(source="get_condition_type_display")

    locations = LocationSerializer(read_only=True)
    rental_info = RentalSerializer(read_only=True, many=True)
    gallery = GallerySerializer(read_only=True, many=True)
    amenities = AmenitiesSerializer(read_only=True, many=True)

    class Meta:
        model = PropertyInfo
        fields = (
            "id",
            "city",
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
            "condition_type",
            "membership_plan",
            "views",
            "price",
            "created_on",
        )


class DetailPropertySerializer(serializers.ModelSerializer):
    """
    This returns property
    """

    class Meta:
        model = PropertyInfo
        fields = (
            "apartment_type",
            "apartment_name",
            "bhk_type",
            "floor",
            "total_floor",
            "age",
            "facing",
            "property_size",
        )


class PropertyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyRequest
        fields = (
            "name",
            "phone",
            "email",
            "request_type",
            "property_type",
            "urgent",
            "place",
            "price_range",
            "size",
            "description",
        )
