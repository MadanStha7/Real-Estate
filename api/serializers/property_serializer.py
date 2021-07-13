from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from property.models import (
    City,
    PropertyCategories,
    PropertyTypes,
    BasicDetails,
    LocalityDetails,
    Locality,
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
    StaffDetailSerializer,
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

    def validate_name(self, name):
        if PropertyCategories.objects.filter(name=name.lower()).exists():
            raise serializers.ValidationError("Name already exists!")
        return name


class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyTypes
        fields = ("id", "name")
        
    def validate_name(self, name):
        if PropertyTypes.objects.filter(name=name.lower()).exists():
            raise serializers.ValidationError("Name already exists!")
        return name


class LocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Locality
        fields = ("id", "name")
        
    def validate_name(self, name):
        if Locality.objects.filter(name=name.lower()).exists():
            raise serializers.ValidationError("Name already exists!")
        return name


class LocalityDetailsSerializer(serializers.ModelSerializer):
    """serialzer to get all location data in rent an sale"""

    locality = LocalitySerializer(many=False, required=False)
    locality_ = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = LocalityDetails
        fields = (
            "id",
            "basic_details",
            "locality",
            "street",
            "locality_",
        )

    @transaction.atomic
    def create(self, validated_data):
        locality = validated_data.get("locality", None)
        # locality_ = validated_data.get("locality_", None)
        if locality is not None:
            locality_data = validated_data.pop("locality")
            locality = Locality.objects.create(name=locality_data["name"])
            locality_details = LocalityDetails.objects.create(
                locality=locality, **validated_data
            )
        else:
            locality_id = validated_data.pop("locality_")
            locality = Locality.objects.get(id=locality_id)
            locality_details = LocalityDetails.objects.create(
                locality=locality, **validated_data
            )

        return locality_details


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
            "advertisement_type_value",
            "city",
            "city_value",
            "property_categories",
            "property_categories_value",
            "property_types",
            "property_types_value",
            "advertisement_type",
            "advertisement_type_value",
            "owner",
            "agent",
            "staff",
            "admin",
            "publish",
            "views",
            "listing_type",
            "listing_type_value",
            "membership_plan",
            "membership_plan_value",
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


class RentalDetailsSerializer(serializers.ModelSerializer):
    """serialzer to get all rental details serialzers"""

    # basic_details = BasicDetailsSerializer(read_only=True)
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
    # id_ = serializers.IntegerField(allow_null=True, write_only=True)
    image = serializers.ListField(
        child=serializers.FileField(max_length=100000), write_only=True
    )
    image_value = serializers.FileField(read_only=True, source="image")

    class Meta:
        # read_only_fields = ["basic_details"]
        model = Gallery
        fields = ["id", "title", "basic_details", "image", "image_value"]

    @transaction.atomic
    def create(self, validated_data):
        print("validated daya")
        image = validated_data.pop("image")
        for img in image:
            print("imagegeg", img)
            gallery = Gallery.objects.create(image=img, **validated_data)
        return gallery


class OwnerSerializer(serializers.Serializer):
    """Serialzers to display a owner details"""

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "full_name",
            "user",
            "phone_number",
            "address",
            "profile_picture",
        )


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
    full_name = serializers.SerializerMethodField(read_only=True)
    phone_number = serializers.SerializerMethodField(read_only=True)

    def get_full_name(self, obj):
        try:
            full_name = UserProfile.objects.get(user=obj.owner).full_name
            return full_name
        except UserProfile.DoesNotExist:
            full_name = None
        return full_name

    def get_phone_number(self, obj):
        try:
            phone_number = UserProfile.objects.get(user=obj.owner).phone_number
            return phone_number
        except UserProfile.DoesNotExist:
            phone_number = None
        return phone_number

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
            "full_name",
            "phone_number",
        )


class AssignPropertySerializer(serializers.ModelSerializer):
    staff = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

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

    basic_details_value = BasicDetailsSerializer(read_only=True)

    class Meta:
        model = SellPropertyDetails
        fields = (
            "id",
            "basic_details",
            "basic_details_value",
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
    basic_details_value = BasicDetailsSerializer(read_only=True)

    class Meta:
        model = ResaleDetails
        fields = (
            "id",
            "basic_details",
            "basic_details_value",
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
        )


class FieldVisitSerializer(serializers.ModelSerializer):
    basic_details = BasicDetailsSerializer(read_only=True)
    basic_details_id = serializers.PrimaryKeyRelatedField(
        queryset=BasicDetails.objects.all(),
        source="basic_details",
        write_only=True,
    )

    class Meta:
        model = FieldVisit
        fields = ("id", "name", "email", "phone", "basic_details", "basic_details_id")

    @transaction.atomic
    def create(self, validated_data):
        print("validated data", validated_data)
        basic_details_data = validated_data.pop("basic_details")
        fieldvisit = FieldVisit.objects.create(
            basic_details=basic_details_data,
            **validated_data,
        )
        return fieldvisit


class DashBoardSerialzer(serializers.Serializer):
    listed_property = serializers.IntegerField()
    sellers = serializers.IntegerField()
    buyers = serializers.IntegerField()
    agents = serializers.IntegerField()
    property_type_commercial = serializers.IntegerField()
    property_type_residential = serializers.IntegerField()
    rental = RentalDetailsSerializer(many=True, read_only=True)
    resale = ResaleDetailsSerializer(many=True, read_only=True)
    basic_details = BasicDetailsSerializer(many=True, read_only=True)


class PropertyRequestSerializer(serializers.ModelSerializer):

    request_type_value = serializers.CharField(
        source="get_request_type_display", read_only=True
    )
    property_type_value = serializers.CharField(
        source="get_property_type_display", read_only=True
    )
    urgent_value = serializers.CharField(source="get_urgent_display", read_only=True)
    staff_value = StaffDetailSerializer(read_only=True)
    description_assigned_to_employee = serializers.CharField()

    class Meta:
        model = PropertyRequest
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "request_type",
            "request_type_value",
            "property_type",
            "property_type_value",
            "urgent",
            "urgent_value",
            "staff",
            "staff_value",
            "due_date",
            "description_assigned_to_employee",
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


class AssignPropertyRequestSerializer(serializers.ModelSerializer):
    staff = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    description_assigned_to_employee = serializers.CharField()

    class Meta:
        model = PropertyRequest
        fields = (
            "id",
            "staff",
            "description_assigned_to_employee",
            "due_date",
        )
