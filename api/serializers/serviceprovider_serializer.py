from django.contrib.auth.models import User
from rest_framework import serializers

from api.serializers.user_serializer import UserProfileSerializer
from service_provider.models import ServiceProvider


class ServiceProviderSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    custom_field = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProvider

        fields = ("user", "users", "username", "service_name", "company_name",
                  "location", "price", "contact_number",
                  "description", "photos_or_videos",
                  "added_at", "custom_field")


    def get_custom_field(self, obj):
        return dict(a=1, b=3)
