from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from api.serializers.user_serializer import (
    UserProfileSerializer,
    AgentDetailSerializer,
    ChangePasswordSerializer,
    UserSerializer,
    UserRegisterSerializer,
    ContactSerializer,
)
from user.models import UserProfile, User, AgentDetail, Contact
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMessage
from project.settings import EMAIL_HOST_USER
from rest_framework.response import Response


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Userprofile details
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class AgentDetailViewSet(viewsets.ModelViewSet):
    """
    Agent details
    """

    queryset = AgentDetail.objects.all()
    serializer_class = AgentDetailSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    user password reset
    """

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterViewSet(viewsets.ModelViewSet):
    """
    User sign up
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class SendMailView(APIView):
    """
    View to send mail to concerned people through contact page
    """

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            name = data.get("name")
            email = data.get("email")
            phone = data.get("phone")
            message = data.get("message")
            print("EMAIL_HOST_USER", EMAIL_HOST_USER)
            send_mail(
                "Sent email from {}".format(name),
                "Here is the message. {}".format(message),
                email,
                [EMAIL_HOST_USER],
                fail_silently=False,
            )
            Contact.objects.create(name=name,email=email,phone=phone,message=message)
            return Response({"success": "Message sent successfully"})
        return Response({"success": "Failed"}, status=status.HTTP_400_BAD_REQUEST)

