from rest_framework.views import APIView

from api.serializers.user_serializer import UserProfileSerializer, AgentDetailSerializer
from user.models import UserProfile, AgentDetail
from user.models import UserProfile
from user.models import AgentDetail



from rest_framework import generics

class UserProfileList(APIView):
    class UserProfileList(generics.ListCreateAPIView):
        queryset = UserProfile.objects.all()
        serializer_class = UserProfileSerializer

    class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset = UserProfile.objects.all()
        serializer_class = UserProfileSerializer



class AgentDetailList(APIView):

    class AgentDetailList(generics.ListCreateAPIView):
        queryset = AgentDetail.objects.all()
        serializer_class = AgentDetailSerializer

    class AgentDetailDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset = AgentDetail.objects.all()
        serializer_class = AgentDetailSerializer