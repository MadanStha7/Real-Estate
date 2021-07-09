from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from property.models import (
    City,
    PropertyCategories,
    PropertyTypes,
    BasicDetails,
    LocalityDetails,
    RentalDetails,
    RentPropertyDetails,
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
from .user_serializer import (
    UserProfileSerializer,
    AdminProfileSerializer,
    UserSerializer,
)
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

class PropertyUserSerializer(serializers.ModelSerializer):
    """
    created to display name of user in property
    """

    username = serializers.CharField(required=False)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
        ]



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

    city_value = CitySerializer(read_only=True, source="city")
    property_categories_value = PropertyCategoriesSerializer(
        read_only=True, source="property_categories"
    )
    property_types_value = PropertyTypeSerializer(
        read_only=True, source="property_types"
    )
    advertisement_type_value = serializers.CharField(
        source="get_advertisement_type_display", read_only=True
    )
    listing_type_value = serializers.CharField(
        source="get_listing_type_display", read_only=True
    )
    membership_plan_value = serializers.CharField(
        source="get_membership_plan_display", read_only=True
    )
    condition_type_value = serializers.CharField(
        source="get_condition_type_display", read_only=True
    )

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
            "advertisement_type_value",
            "owner",
            "agent",
            "staff",
            "admin",
            "publish",
            "views",
            "listing_type",
            "membership_plan",
            "condition_type",
            "listing_type_value",
            "membership_plan_value",
            "condition_type_value",
        )


class RentPropertyDetailsSerializer(serializers.ModelSerializer):
    bhk_type_value = serializers.CharField(
        source="get_bhk_type_display", read_only=True
    )
    facing_direction_value = serializers.CharField(
        source="get_facing_direction_display", read_only=True
    )

    class Meta:
        model = RentPropertyDetails
        fields = (
            "id",
            "basic_details",
            "bhk_type",
            "floor_number",
            "total_floors",
            "property_age",
            "facing_direction",
            "property_size",
            "bhk_type_value",
            "facing_direction_value",
        )


class LocalityDetailsSerializer(serializers.ModelSerializer):
    """serialzer to get all location data in rent an sale"""

    class Meta:
        model = LocalityDetails
        fields = (
            "id",
            "basic_details",
            "locality",
            "street",
            "location",
        )


class RentalDetailsSerializer(serializers.ModelSerializer):
    """serialzer to get all rental details serialzers"""

    price_value = serializers.CharField(source="get_price_display", read_only=True)
    furnishing_value = serializers.CharField(
        source="get_furnishing_display", read_only=True
    )
    no_of_parking_value = serializers.CharField(
        source="get_no_of_parking_display", read_only=True
    )

    class Meta:
        model = RentalDetails
        fields = (
            "id",
            "basic_details",
            "expected_rent",
            "expected_deposit",
            "price",
            "price_value",
            "available_from",
            "furnishing",
            "furnishing_value",
            "no_of_parking",
            "description",
            "no_of_parking_value",
        )


class GallerySerializer(serializers.ModelSerializer):
    """serialzer to get all gallery serialzers"""

    class Meta:
        model = Gallery
        fields = (
            "id",
            "title",
            "image",
            "basic_details",
        )


# class FilteredListSerializer(serializers.ListSerializer):
#     """Serialzers to display a ph number of user"""

#     def to_representation(self, data):
#         print("data################",data)
#         data = data.filter(user=self.context['request'].user, edition__hide=False)
#         return super(FilteredListSerializer, self).to_representation(data)


class PendingPropertySerializer(serializers.ModelSerializer):
    """
    serialzer for all pending property display
    """

    city_value = CitySerializer(read_only=True, source="city")
    property_categories_value = PropertyCategoriesSerializer(
        read_only=True, source="property_categories"
    )
    property_types_value = PropertyTypeSerializer(
        read_only=True, source="property_types"
    )
    advertisement_type_value = serializers.CharField(
        source="get_advertisement_type_display", read_only=True
    )
    listing_type_value = serializers.CharField(
        source="get_listing_type_display", read_only=True
    )
    membership_plan_value = serializers.CharField(
        source="get_membership_plan_display", read_only=True
    )
    condition_type_value = serializers.CharField(
        source="get_condition_type_display", read_only=True
    )
    owner = UserSerializer(read_only=True)
    rent_property = RentPropertyDetailsSerializer(many=True, read_only=True)
    location = LocalityDetailsSerializer(read_only=True)
    # customer = serializers.SerializerMethodField()

    # def get_customer(self,obj):
    #     print("obj",obj.owner.id)
    #     try:
    #         user_data = UserProfile.objects.get(user__id=obj.owner.id)
    #         user = UserProfileSerializer(user_data, many=True)
    #         print('user',user)
    #     except UserProfile.DoesNotExist:
    #         user = None
    #     return user

    class Meta:
        # list_serializer_class = FilteredListSerializer
        model = BasicDetails
        fields = (
            "id",
            "advertisement_type",
            "city",
            "city_value",
            "location",
            "property_categories",
            "property_categories_value",
            "property_types_value",
            "property_types",
            "advertisement_type",
            "advertisement_type_value",
            "owner",
            "agent",
            "staff",
            "admin",
            "publish",
            "views",
            "listing_type",
            "membership_plan",
            "condition_type",
            "listing_type_value",
            "membership_plan_value",
            "condition_type_value",
            "rent_property",
            # "customer"
        )


class AssignPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicDetails
        fields = (
            "id",
            "staff",
            "due_date",
            "description",
        )


class SellPropertyDetailsSerializer(serializers.ModelSerializer):
    bhk_type_value = serializers.CharField(
        source="get_bhk_type_display", read_only=True
    )
    total_floors_value = serializers.CharField(
        source="get_total_floors_display", read_only=True
    )
    property_age_value = serializers.CharField(
        source="get_property_age_display", read_only=True
    )
    facing_direction_value = serializers.CharField(
        source="get_facing_direction_display", read_only=True
    )

    basic_details = BasicDetailsSerializer(read_only=True)

    class Meta:
        model = SellPropertyDetails
        fields = (
            "id",
            "basic_details",
            "bhk_type",
            "bhk_type_value",
            "total_floors",
            "total_floors_value",
            "property_age",
            "property_age_value",
            "built_up_area",
            "property_size",
            "facing_direction",
            "facing_direction_value",
        )


class ResaleDetailsSerializer(serializers.ModelSerializer):
    price_value = serializers.CharField(source="get_price_display", read_only=True)
    kitchen_type_value = serializers.CharField(
        source="get_kitchen_type_display", read_only=True
    )
    furnishing_value = serializers.CharField(
        source="get_furnishing_display", read_only=True
    )
    no_of_parking_value = serializers.CharField(
        source="get_no_of_parking_display", read_only=True
    )
    construction_type_value = serializers.CharField(
        source="get_construction_type_display", read_only=True
    )
    basic_details = BasicDetailsSerializer(read_only=True)

    class Meta:
        model = ResaleDetails
        fields = (
            "id",
            "basic_details",
            "expected_price",
            "price",
            "price_value",
            "available_from",
            "kitchen_type",
            "kitchen_type_value",
            "furnishing",
            "furnishing_value",
            "no_of_parking",
            "no_of_parking_value",
            "construction_type",
            "construction_type_value",
            "pillar_size_width1",
            "pillar_size_width2",
            "description",
        )


class AmenitiesSerializer(serializers.ModelSerializer):
    basic_details = BasicDetailsSerializer(read_only=True)

    class Meta:
        model = Amenities
        fields = (
            "id",
            "basic_details",
            "total_no_bathrooms",
            "water_supply",
            "swimming_pool",
            "security",
            "gym",
            "lift",
            "title",
            "image",
        )

class PropertyDiscussionSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    user = PropertyUserSerializer(read_only=True)

    class Meta:
        model = PropertyDiscussionBoard
        fields = (
            "id",
            "discussion",
            "title",
            "tags",
            "comments",
            "basic_details",
            "user",
            "user_id",
        )

    
