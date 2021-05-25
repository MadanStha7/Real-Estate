import random
import uuid
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import login, authenticate, logout
from api.serializers.user_serializer import (
    UserProfileSerializer,
    AgentDetailSerializer,
    ChangePasswordSerializer,
    UserSerializer,
    ContactSerializer,
    OtpSerializer,
    UserLoginSerializer,
    StaffDetailSerializer,
    AdminProfileSerializer,
)
from rest_framework.authtoken.models import Token
from user.models import UserProfile, AgentDetail, Contact, StaffDetail, AdminProfile
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMessage
from project.settings import EMAIL_HOST_USER
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, views, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Userprofile details including buyer and seller
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer

    def perform_create(self, serializer):
        print("executed")
        serializer = AdminProfileSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"True"}, status=status.HTTP_201_CREATED)
        return Response("serializer errors", status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == "POST":
            context.update(
                {
                    "request": self.request.method,
                }
            )
        return context

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class AgentDetailViewSet(viewsets.ModelViewSet):
    """
    Agent details
    """

    queryset = AgentDetail.objects.all()
    serializer_class = AgentDetailSerializer

    def perform_create(self, serializer):
        serializer = AgentDetailSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"True"}, status=status.HTTP_201_CREATED)
        return Response("serializer errors", status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        print("data****************", self.request.data)
        context = super().get_serializer_context()
        context.update(
            {
                "request": self.request.method,
            }
        )
        print("context", context)
        return context


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


class StaffDetailViewset(viewsets.ModelViewSet):
    """
    This view returns the list and creation of staff
    """

    queryset = StaffDetail.objects.all()
    serializer_class = StaffDetailSerializer

    def perform_create(self, serializer):
        print("data", self.request.data)
        serializer = StaffDetailSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"True"}, status=status.HTTP_201_CREATED)
        return Response("serializer errors", status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == "POST":
            print("ram thapa")
            context.update(
                {
                    "request": self.request.method,
                }
            )
            print("context", context)
        return context

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class UserLoginView(APIView):
    """This view returns the login of user"""

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            try:
                u_name = data.get("username_or_email", None)
                pword = data.get("password", None)
                user = authenticate(username=u_name, password=pword)
                if user:
                    try:
                        token = Token.objects.get(user=user.id)
                        print("token", token)
                    except Token.DoesnoDoesNotExist:
                        return Response(
                            {"Invalid": "Unauthenticated user"},
                            status=status.HTTP_404_NOT_FOUND,
                        )
                    if user is not None:
                        if user.is_active:
                            return Response(
                                {
                                    "Success": "User successfully logged in.",
                                    "token": token.key,
                                    "id": user.id,
                                },
                                status=status.HTTP_200_OK,
                            )
                        else:
                            return Response(status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response(
                            "User doesn't exist", status=status.HTTP_404_NOT_FOUND
                        )
                else:
                    return Response(
                        {"error": "User doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid Credential"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response("Field is required", status=status.HTTP_404_NOT_FOUND)


class OtpVerify(APIView):
    """otp verification"""

    def post(self, request, format=None):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            otp = data.get("otp_code")
            u_id = data.get("user_id")
            try:
                # get the user id
                user_profile = UserProfile.objects.get(user_id=u_id)
                old_otp = user_profile.otp_code
                if otp != old_otp:
                    return Response(
                        {"Otp": "Invalid otp"}, status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                else:
                    user_profile.is_email = True
                    user_profile.is_phone = True
                    user_profile.save()
                    return Response(
                        {
                            "Verify success": "Your account has been successfully activated!!"
                        },
                        status=status.HTTP_202_ACCEPTED,
                    )

            except UserProfile.DoesnotExist:
                return Response(
                    {
                        "No User": "Invalid otp OR No any inactive user found for given otp"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


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
            send_mail(
                "Sent email from {}".format(name),
                "Here is the message. {}".format(message),
                email,
                [EMAIL_HOST_USER],
                fail_silently=False,
            )
            Contact.objects.create(name=name, email=email, phone=phone, message=message)
            return Response({"success": "Message sent successfully"})
        return Response({"success": "Failed"}, status=status.HTTP_400_BAD_REQUEST)
