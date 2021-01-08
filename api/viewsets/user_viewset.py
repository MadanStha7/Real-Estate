from rest_framework import viewsets

from api.serializers.user_serializer import UserProfileSerializer, AgentDetailSerializer, ChangePasswordSerializer
from user.models import UserProfile, User
from user.models import AgentDetail


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class AgentDetailViewSet(viewsets.ModelViewSet):
    queryset = AgentDetail.objects.all()
    serializer_class = AgentDetailSerializer


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer