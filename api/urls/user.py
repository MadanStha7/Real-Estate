from django.urls import include, path
from rest_framework import routers
from api.viewsets.user_viewset import UserProfileViewSet, AgentDetailViewSet


router = routers.DefaultRouter()
router.register(r'user-profile', UserProfileViewSet)
router.register(r'agent-detail', AgentDetailViewSet)


urlpatterns = [
    path('user', include(router.urls)),
]
