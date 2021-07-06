from django.db.models.query import QuerySet
from rest_framework import serializers
from property.models import (
    City,
    PropertyCategories,
    PropertyTypes,
    BasicDetails,
    Location,
    RentalDetails,
    Gallery,
    SellPropertyDetails,
    ResaleDetails,
    Amenities,
    FieldVisit,
    PropertyDiscussionBoard,
    PropertyRequest,
    ContactAgent,
    Comment,
    Reply,
)
from .user_serializer import UserProfileSerializer, AdminProfileSerializer
from user.models import (
    UserProfile,
    AgentDetail,
    StaffDetail,
    AdminProfile,
    Notificatons,
)
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import datetime, timezone

User = get_user_model()


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")

    def validate_name(self, name):
        if City.objects.filter(name=name.lower()).exists():
            raise serializers.ValidationError("City name already exists!")
        return name


class PropertyCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyCategories
        fields = ("id", "name")


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyTypes
        fields = ("id", "name")


class BasicDetailsSerializer(serializers.ModelSerializer):
    """
    serialzer for basic details for rent and sale
    """

    city_value = CitySerializer(read_only=True)
    property_categories_value = PropertyCategoriesSerializer(read_only=True)
    property_types_value = PropertyTypeSerializer(read_only=True)

    class Meta:
        model = BasicDetails
        fields = (
            "id",
            "advertisement_type",
            "city",
            "city_value",
            "property_categories",
            "property_categories_value",
            "property_types_value",
            "property_types",
            "advertisement_type",
            "owner",
            "agent",
            "staff",
            "admin",
            "publish",
            "views",
            "listing_type",
            "membership_plan",
            "condition_type",
        )


class SellPropertyDetailsSerializer(serializers.ModelSerializer):
    bhk_type_value = serializers.CharField(
        source="get_bhk_type_display", read_only=True)
    total_floors_value = serializers.CharField(
        source="get_total_floors_display", read_only=True)
    property_age_value = serializers.CharField(
        source="get_property_age_display", read_only=True)
    facing_direction_value = serializers.CharField(
        source="get_facing_direction_display", read_only=True)

    basic_details = BasicDetailsSerializer(read_only=True)

    class Meta:
        model = SellPropertyDetails
        fields = (
            'id',
            'basic_details',
            'bhk_type',
            "bhk_type_value",
            "total_floors",
            "total_floors_value",
            'property_age',
            'property_age_value',
            'built_up_area',
            'property_size',
            'facing_direction',
            "facing_direction_value"
        )


class ResaleDetailsSerializer(serializers.ModelSerializer):
    price_value = serializers.CharField(
        source="get_price_display", read_only=True)
    kitchen_type_value = serializers.CharField(
        source="get_kitchen_type_display", read_only=True)
    furnishing_value = serializers.CharField(
        source="get_furnishing_display", read_only=True)
    no_of_parking_value = serializers.CharField(
        source="get_no_of_parking_display", read_only=True)
    construction_type_value = serializers.CharField(
        source="get_construction_type_display", read_only=True)
    basic_details = BasicDetailsSerializer(read_only=True)

    class Meta:
        model = ResaleDetails
        fields = (
            'id',
            "basic_details",
            'expected_price',
            'price',
            'price_value',
            'available_from',
            'kitchen_type',
            'kitchen_type_value',
            'furnishing',
            'furnishing_value',
            'no_of_parking',
            'no_of_parking_value',
            'construction_type',
            'construction_type_value',
            "pillar_size_width1",
            "pillar_size_width2",
            'description',
        )


class AmenitiesSerializer(serializers.ModelSerializer):
    basic_details = BasicDetailsSerializer(read_only=True)

    class Meta:
        model = Amenities
        fields = (
            'id',
            'basic_details',
            'total_no_bathrooms',
            'water_supply',
            'swimming_pool',
            'security',
            'gym',
            'lift',
            'title',
            'image'
        )
