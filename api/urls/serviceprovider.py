from django.urls import include, path
from rest_framework import routers
from api.viewsets.serviceprovider_viewset import ServiceProviderViewSet

router = routers.DefaultRouter()
router.register(r'service', ServiceProviderViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
