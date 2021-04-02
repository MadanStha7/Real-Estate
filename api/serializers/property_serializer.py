from rest_framework import serializers
from property.models import PropertyInfo, Gallery, FieldVisit, PropertyDiscussionBoard, RentalInfo, Amenities
from user.models import UserProfile, AgentDetail

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model=Gallery
        fields=(
            "id", "image", "video"
        )
class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Amenities
        fields=(
            "id", "bathrooms","balcony",
            'water_supply',"gym","non_veg",
            "security","viewer","secondary_number"
        )
class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model=RentalInfo
        fields = (
            "id", "available_for","expected_rent",
            "expected_deposit","negotiable",
            "maintenance","available_from",
            "tenants","furnishing",
            "parking","description"
        )
class PropertySerializer(serializers.ModelSerializer):
    gallery= GallerySerializer(many=True, read_only=True)
    rental=RentalSerializer(read_only=True)
    amenities=AmenitiesSerializer(many=True, read_only=True)
    owner= serializers.CharField(source="owner.user")
    agent=serializers.CharField(source="agent.user")
    class Meta:
        model = PropertyInfo
        fields = (
            "id", "property_type", "property_adtype",
            "apartment_type", "apartment_name",
            "bhk_type","floor","total_floor",
            "age","facing","property_size",
            "city","locality","street","rental",
            "gallery","amenities","owner", "agent",
            "staff","location","latitude","longitude"
                  )

    def get_custom_field(self, obj):
        return dict(a=1, b=3, uid=obj.uid)


    def create(self, validated_data):
        amenities_data=validated_data.pop("amenities")
        amenities=Amenities.objects.create(**amenities_data)
        validated_data['amenities']=amenities
        property_info=PropertyInfo.objects.create(**validated_data)
        return property_info


class FieldVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldVisit
        fields = ('id', 'name', 'email', 'phone', 'property_type')


class PropertyDiscussionSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = PropertyDiscussionBoard
        fields = ('id', 'discussion', 'title', 'tags', 'comments', 'property_type')


