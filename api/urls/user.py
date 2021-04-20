from django.urls import include, path
from rest_framework import routers
from api.viewsets.user_viewset import UserProfileViewSet, AgentDetailViewSet, \
    ChangePasswordView, UserViewSet, \
    ContactViewSet, SendMailView, RegisterView, OtpVerify, UserLoginView

router = routers.DefaultRouter()
router.register(r'buyer_seller_profile', UserProfileViewSet)
router.register(r'agent-detail', AgentDetailViewSet)
router.register(r'all_users', UserViewSet)
router.register(r'contact', ContactViewSet)


urlpatterns = [
    # login page
    path('user-login/', UserLoginView.as_view(), name='user_login'),
    path("register/", RegisterView.as_view(), name='register'),
    path('otp-verify/', OtpVerify.as_view(), name="otp_verify"),


    path('user/', include(router.urls)),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(),
         name='auth_change_password'),

    # contact page for sending email
    path('send-mail/', SendMailView.as_view(), name='send-mail'),
]
