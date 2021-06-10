from django.urls import include, path
from rest_framework import routers
from api.viewsets.user_viewset import (
    UserProfileViewSet,
    AgentDetailViewSet,
    ChangePasswordView,
    UserViewSet,
    ContactViewSet,
    SendMailView,
    OtpVerify,
    UserLoginView,
    StaffDetailViewset,
    AdminProfileViewSet,
    AdminViewSet,
    LogoutView,
    MyProfileView,
    AgentSearchViewSet,
)

router = routers.DefaultRouter()
router.register(r"user_profile", UserProfileViewSet)
router.register(r"agent_detail", AgentDetailViewSet)
router.register(r"admin", AdminViewSet)
router.register(r"staff", StaffDetailViewset)
router.register(r"all_users", UserViewSet)
router.register(r"contact", ContactViewSet)
router.register(r"admin_profile", AdminProfileViewSet)
router.register(r"my_profile", MyProfileView)
router.register(r"agent-search", AgentSearchViewSet)


urlpatterns = [
    # login page
    path("user-login/", UserLoginView.as_view(), name="user_login"),
    path("otp-verify/", OtpVerify.as_view(), name="otp_verify"),
    path("user/", include(router.urls)),
    path(
        "change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    # contact page for sending email
    path("send-mail/", SendMailView.as_view(), name="send-mail"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
