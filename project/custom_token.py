from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from user.models import AgentDetail, UserProfile, AdminProfile, StaffDetail
from django.contrib.auth import get_user_model

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
        except AgentDetail.DoesNotExist:
            pass
        try:
            user_details = StaffDetail.objects.get(user=user_obj)
            full_name = user_details.full_name
        except StaffDetail.DoesNotExist:
            pass

        try:
            user_details = UserProfile.objects.get(user=user_obj)
            full_name = user_details.full_name

        except UserProfile.DoesNotExist:
            pass
        try:
            user_details = AdminProfile.objects.get(user=user_obj)
            full_name = user_details.full_name

        except AdminProfile.DoesNotExist:
            pass

        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "full_name": full_name,
            }
        )
