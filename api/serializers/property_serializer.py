from django.db.models.query import QuerySet
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
    ContactAgent,
    FloorPlan,
    Comment,
    Reply,
)
from .user_serializer import UserProfileSerializer, AdminProfileSerializer
from user.models import UserProfile, AgentDetail, StaffDetail, AdminProfile
from django.db import transaction
from django.contrib.auth import get_user_model

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


class LocationSerializer(serializers.ModelSerializer):
    """
    Location of property info
    """

    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source="city", write_only=True
    )
    city = CitySerializer(read_only=True)

    class Meta:
        model = Location
        fields = ("id", "city_id", "city", "locality", "street", "property_info")


class PropertySerializer(serializers.ModelSerializer):
    """
    return the property details in homepage in client side
    """

    listing_type = serializers.CharField(required=False)
    membership_plan = serializers.CharField(required=False)
    condition_type = serializers.CharField(required=False)
    created_on = serializers.CharField(read_only=True)
    locations = LocationSerializer(read_only=True)
    gallery = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="gallery-detail"
    )
    facing = serializers.CharField(required=False)

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
            "locations",
            "latitude",
            "longitude",
            "publish",
            "views",
            "listing_type",
            "membership_plan",
            "condition_type",
            "description",
            "price",
            "status",
            "created_on",
            "gallery",
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


# class LocationSerializer(serializers.ModelSerializer):
#     """
#     Location of property info
#     """

#     city_id = serializers.PrimaryKeyRelatedField(
#         queryset=City.objects.all(),
#         source="city",
#         write_only=True,
#     )
#     city = CitySerializer(read_only=True)

#     class Meta:
#         model = Location
#         fields = (
#             "id",
#             "city",
#             "city_id",
#             "locality",
#             "street",
#             "listing",
#             "property_info",
#         )


class GallerySerializer(serializers.ModelSerializer):
    """
    gallery of property info
    """

    property_info_value = PropertySerializer(read_only=True)

    class Meta:
        model = Gallery
        fields = (
            "id",
            "title",
            "image",
            "link",
            "property_info",
            "property_info_value",
        )


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
            "property_type",
            "user",
            "user_id",
        )

    @transaction.atomic
    def create(self, validated_data):
        discussion_board = PropertyDiscussionBoard.objects.create(**validated_data)
        Comment.objects.create(
            discussion_board=discussion_board,
            user=validated_data["user"],
            text=validated_data["comments"],
        )
        return discussion_board


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
    city = CitySerializer(read_only=True)

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
            "status",
            "created_on",
        )


class FieldVisitSerializer(serializers.ModelSerializer):
    property_type = PropertyDetailSerializer(read_only=True)
    property_type_id = serializers.PrimaryKeyRelatedField(
        queryset=PropertyInfo.objects.all(),
        source="property_type",
        write_only=True,
    )

    class Meta:
        model = FieldVisit
        fields = ("id", "name", "email", "phone", "property_type", "property_type_id")

    @transaction.atomic
    def create(self, validated_data):
        print("validated data", validated_data)
        property_type_data = validated_data.pop("property_type")
        fieldvisit = FieldVisit.objects.create(
            property_type=property_type_data,
            **validated_data,
        )
        return fieldvisit


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
    request_type_display = serializers.CharField(
        source="get_request_type_display", required=False
    )
    property_type_display = serializers.CharField(
        source="get_property_type_display", required=False
    )
    urgent_display = serializers.CharField(source="get_urgent_display", required=False)
    urgent = serializers.CharField(required=False)

    class Meta:
        model = PropertyRequest
        fields = (
            "name",
            "phone",
            "email",
            "request_type",
            "request_type_display",
            "property_type",
            "property_type_display",
            "urgent_display",
            "urgent",
            "place",
            "price_range",
            "size",
            "description",
        )


class PropertyTypeFilteredSerialzers(serializers.Serializer):
    """Serialzers fields for sending fileterd data in response for admin dashboard"""

    property_type_commercial = serializers.IntegerField()
    property_type_residential = serializers.IntegerField()
    total_property = serializers.IntegerField()
    sellers = serializers.IntegerField()
    buyers = serializers.IntegerField()


class ContactAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactAgent
        fields = ("id", "name", "email", "property_info", "agent")


class FloorPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorPlan
        fields = ("id", "property_type", "name", "file")


class ReplySerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    # reply_ = serializers.SerializerMethodField(read_only=True)

    def get_full_name(self, obj):
        if obj:
            user_obj = obj.reply_madeby
            try:
                user_details = user_obj.agent_detail.full_name
                return user_details
            except AgentDetail.DoesNotExist:
                pass
            try:
                user_details = user_obj.buyer_seller_profile.full_name
                return user_details
            except UserProfile.DoesNotExist:
                pass

            try:
                user_details = user_obj.staff_detail.full_name
                return user_details
            except StaffDetail.DoesNotExist:
                pass
            try:
                user_details = user_obj.admin.full_name
                return user_details

            except AdminProfile.DoesNotExist:
                pass

    class Meta:
        model = Reply
        fields = (
            "id",
            "reply_madeby",
            "reply_madeto",
            "comment",
            "reply",
            "created_on",
            "full_name",
        )


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    discussion_board_id = serializers.PrimaryKeyRelatedField(
        queryset=PropertyDiscussionBoard.objects.all(),
        source="discussion_board",
        write_only=True,
    )
    discussion_board = PropertyDiscussionSerializer(read_only=True)
    user_details = serializers.SerializerMethodField(read_only=True)
    reply = ReplySerializer(many=True, read_only=True)

    created_on = serializers.DateTimeField(read_only=True)

    def get_user_details(self, obj):
        if obj:
            user_obj = obj.user
            try:
                user_details = user_obj.agent_detail.full_name
                return user_details
            except AgentDetail.DoesNotExist:
                pass
            try:
                user_details = user_obj.buyer_seller_profile.full_name
                return user_details
            except UserProfile.DoesNotExist:
                pass

            try:
                user_details = user_obj.staff_detail.full_name
                return user_details
            except StaffDetail.DoesNotExist:
                pass
            try:
                user_details = user_obj.admin.full_name
                return user_details

            except AdminProfile.DoesNotExist:
                pass
            # return

    class Meta:
        model = Comment
        fields = (
            "id",
            "user_id",
            "discussion_board_id",
            "text",
            "user",
            "discussion_board",
            "created_on",
            "user_details",
            "reply",
        )
