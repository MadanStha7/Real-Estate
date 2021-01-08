from django.urls import include, path
from rest_framework import routers
from api.viewsets.user_viewset import UserProfileViewSet, AgentDetailViewSet,ChangePasswordView



router = routers.DefaultRouter()
router.register(r'user-profile', UserProfileViewSet)
router.register(r'agent-detail', AgentDetailViewSet)


urlpatterns = [
    path('user', include(router.urls)),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]
