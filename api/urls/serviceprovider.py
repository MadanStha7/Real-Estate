from django.urls import include, path
from rest_framework import routers
from api.viewsets.serviceprovider_viewset import ServiceProviderViewSet, BusinessHourViewSet

router = routers.DefaultRouter()
router.register(r'service', ServiceProviderViewSet)
router.register(r'business_hour', BusinessHourViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
