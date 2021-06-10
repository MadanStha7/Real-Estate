from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from user.models import AgentDetail, UserProfile, AdminProfile, StaffDetail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status

User = get_user_model()


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user_obj = User.objects.get(id=user.id)
        try:
            user_details = AgentDetail.objects.get(user=user_obj)
            full_name = user_details.full_name
            image = None
        except AgentDetail.DoesNotExist:
            pass
        try:
            user_details = StaffDetail.objects.get(user=user_obj)
            full_name = user_details.full_name
            image = None

        except StaffDetail.DoesNotExist:
            pass

        try:
            user_details = UserProfile.objects.get(user=user_obj)
            full_name = user_details.full_name
            if user_details.is_email:
                pass
            else:
                return Response(
                    {"Invalid": "Unauthenticated user"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if user_details.profile_picture:
                image = user_details.profile_picture.url
            else:
                image = None
        except UserProfile.DoesNotExist:
            pass
        try:
            user_details = AdminProfile.objects.get(user=user_obj)
            full_name = user_details.full_name
            if user_details.image:
                image = user_details.image.url
            else:
                image = None
        except AdminProfile.DoesNotExist:
            pass

        token, created = Token.objects.get_or_create(user=user)
        group_name = Group.objects.filter(user=user).values()
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "full_name": full_name,
                "image": image,
                "group_name": group_name,
            }
        )
