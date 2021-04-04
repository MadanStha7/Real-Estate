from rest_framework import serializers
from property.models import (
    PropertyInfo,
    Gallery,
    FieldVisit,
    PropertyDiscussionBoard,
    RentalInfo,
    Amenities,
    Schedule,
)
from user.models import UserProfile, AgentDetail


class PropertySerializer(serializers.ModelSerializer):
    # gallery = GallerySerializer(read_only=True)
    # rental = RentalSerializer(read_only=True)
    # amenities = AmenitiesSerializer(read_only=True)
    # owner = serializers.CharField(source="owner.user", required=False)
    # agent = serializers.CharField(source="agent.user", required=False)

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
            "city",
            "locality",
            "street",
            "rental",
            "gallery",
            "amenities",
            "owner",
            "agent",
            "staff",
            "location",
            "latitude",
            "longitude",
        )

    def create(self, validated_data):
        gallery = validated_data.pop('gallery')
        rental = validated_data.pop('rental')
        amenities = validated_data.pop('amenities')
        property_info = PropertyInfo.objects.create(rental=rental,amenities=amenities, **validated_data)
        for ga in gallery:
            property_info.gallery.add(ga)
        return property_info
    

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ("id", "image", "video")



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
        )


class RentalSerializer(serializers.ModelSerializer):
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

