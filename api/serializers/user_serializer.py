from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import AgentDetail, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'is_superuser')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class AgentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentDetail
        fields = '__all__'


