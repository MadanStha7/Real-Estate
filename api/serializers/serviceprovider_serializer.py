from django.contrib.auth.models import User
from rest_framework import serializers

from api.serializers.user_serializer import UserSerializer
from service_provider.models import ServiceProvider, Review, BusinessHours


class BusinessHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = ("id", "day", "opening_time", "closing_time")


class ServiceProviderSerializer(serializers.ModelSerializer):
    business_hours = BusinessHourSerializer(read_only=True, many=True)
    username = serializers.CharField(source="user.username", read_only=True)
    custom_field = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = ServiceProvider
        read_only_fields = ["photos_or_videos", "user"]

        fields = (
            "id",
            "user",
            "username",
            "service_name",
            "company_name",
            "address",
            "price",
            "contact_number",
            "description",
            "photos_or_videos",
            "added_at",
            "location",
            "latitude",
            "longitude",
            "business_hours",
            "custom_field",
        )

    def get_custom_field(self, obj):
        return dict(a=1, b=3)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        validated_data["user"] = user
        service_provider = ServiceProvider.objects.create(**validated_data)
        return service_provider

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user")
        user = instance.user
        instance.service_name = validated_data.get(
            "service_name", instance.service_name
        )
        instance.company_name = validated_data.get(
            "company_name", instance.company_name
        )
        instance.address = validated_data.get("address", instance.address)
        instance.location = validated_data.get("location", instance.location)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.price = validated_data.get("price", instance.price)
        instance.contact_number = validated_data.get(
            "contact_number", instance.contact_number
        )
        instance.description = validated_data.get("description", instance.description)
        instance.photos_or_videos = validated_data.get(
            "photos_or_videos", instance.photos_or_videos
        )
        instance.added_at = validated_data.get("added_at ", instance.added_at)

        user.id = user_data.get("id", user.id)
        user.username = user_data.get("username", user.username)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.is_staff = user_data.get("is_staff", user.is_staff)
        user.is_superuser = user_data.get("is_superuser", user.is_superuser)
        user.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    user = UserSerializer()

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "username",
            "service_provider",
            "date",
            "rating",
            "description",
            "recommend",
        )

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        validated_data["user"] = user
        review = Review.objects.create(**validated_data)
        return review

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user")
        user = instance.user
        user.id = user_data.get("id", user.id)
        user.username = user_data.get("username", user.username)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.is_staff = user_data.get("is_staff", user.is_staff)
        user.is_superuser = user_data.get("is_superuser", user.is_superuser)
        user.save()
        return instance
