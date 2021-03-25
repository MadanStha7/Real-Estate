from django.urls import include, path
from rest_framework import routers
from api.viewsets.serviceprovider_viewset import ServiceProviderViewSet, \
    ReviewViewSet, BusinessHourViewSet

router = routers.DefaultRouter()
router.register(r'service', ServiceProviderViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'business_hours', BusinessHourViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
