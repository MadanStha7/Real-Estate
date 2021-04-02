from django.contrib.auth.models import User
from rest_framework import serializers

from api.serializers.property_serializer import PropertySerializer
from api.serializers.serviceprovider_serializer import ServiceProviderSerializer


class PropertyServiceSerializer(serializers.Serializer):
    property_info = PropertySerializer(read_only=True, many=True)
    service_info = ServiceProviderSerializer(read_only=True, many=True)