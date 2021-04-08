from django.urls import include, path
from rest_framework import routers
from api.viewsets.user_viewset import UserProfileViewSet, AgentDetailViewSet, \
    ChangePasswordView, UserViewSet, \
    UserRegisterViewSet,ContactViewSet

router = routers.DefaultRouter()
router.register(r'buyer_seller_profile', UserProfileViewSet)
router.register(r'agent-detail', AgentDetailViewSet)
router.register(r'all_users', UserViewSet)
router.register(r'register', UserRegisterViewSet)
router.register(r'contact', ContactViewSet)



urlpatterns = [
    path('user/', include(router.urls)),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]
