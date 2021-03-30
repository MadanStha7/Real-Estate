from django.contrib.auth.models import User
from rest_framework import serializers

from api.serializers.user_serializer import UserSerializer
from service_provider.models import ServiceProvider, BusinessHour


class BusinessHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHour
        fields = ('id', 'service_provider', 'day', 'opening_time', 'closing_time', 'status')

    def create(self, validated_data):
        business_hour = BusinessHour.objects.create(**validated_data)
        return business_hour

    def update(self, instance, validated_data):
        instance.day = validated_data.get(
            'day', instance.day)
        instance.opening_time = validated_data.get(
            'opening_time', instance.opening_time)
        instance.closing_time = validated_data.get(
            'closing_time', instance.closing_time)
        instance.status = validated_data.get(
            'status', instance.status)

        instance.save()
        return instance


class ServiceProviderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    custom_field = serializers.SerializerMethodField()
    user = UserSerializer()
    service_business_hour = BusinessHourSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceProvider
        read_only_fields = ['photos_or_videos']

        fields = ("user", "username", "service_name", "company_name",
                  "location", "price", "contact_number",
                  "description", "photos_or_videos",
                  "added_at", "service_business_hour", "custom_field")

    def get_custom_field(self, obj):
        return dict(a=1, b=3)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        validated_data['user'] = user
        serviceprovider = ServiceProvider.objects.create(**validated_data)
        return serviceprovider

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.service_name = validated_data.get(
            'service_name', instance.service_name)
        instance.company_name = validated_data.get(
            'company_name', instance.company_name)
        instance.location = validated_data.get(
            'location', instance.location)
        instance.price = validated_data.get(
            'price', instance.price)
        instance.contact_number = validated_data.get(
            'contact_number', instance.contact_number)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.photos_or_videos = validated_data.get(
            'photos_or_videos', instance.photos_or_videos)
        instance.added_at = validated_data.get(
            'added_at ', instance.added_at)

        user.id = user_data.get(
            'id', user.id)
        user.username = user_data.get(
            'username', user.username)
        user.first_name = user_data.get(
            'first_name', user.first_name)
        user.last_name = user_data.get(
            'last_name', user.last_name)
        user.is_staff = user_data.get(
            'is_staff', user.is_staff)
        user.is_superuser = user_data.get(
            'is_superuser', user.is_superuser)
        user.save()
        return instance
