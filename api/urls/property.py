from django.urls import include, path
from rest_framework import routers
from api.viewsets.property_viewset import AmenitiesViewSet, PropertyViewSet, PropertyGalleryViewSet, FieldVisitViewSet, \
    PropertyDiscussionViewSet

router = routers.DefaultRouter()
router.register(r'amenities', AmenitiesViewSet)
router.register(r'property', PropertyViewSet)
router.register(r'property_gallery', PropertyGalleryViewSet)
router.register(r'field_visit', FieldVisitViewSet)
router.register(r'property_discussion', PropertyDiscussionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
