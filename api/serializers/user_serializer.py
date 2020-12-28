from rest_framework import serializers
from user.models import AgentDetail, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class AgentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentDetail
        fields = '__all__'


