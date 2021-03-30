from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from api.serializers.user_serializer import UserProfileSerializer, \
    AgentDetailSerializer, ChangePasswordSerializer, \
    UserSerializer, UserRegisterSerializer
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
