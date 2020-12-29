from django.urls import include, path
from rest_framework import routers
from api.viewsets.property_viewset import AmenitiesViewSet, PropertyViewSet, PropertyGalleryViewSet, FieldVisitViewSet, \
    PropertyDiscussionViewSet

router = routers.DefaultRouter()
router.register(r'Amenities', AmenitiesViewSet)
router.register(r'Property', PropertyViewSet)
router.register(r'PropertyGallery', PropertyGalleryViewSet)
router.register(r'FieldVisit', FieldVisitViewSet)
router.register(r'PropertyDiscussion', PropertyDiscussionViewSet)


urlpatterns = [
    path('Property', include(router.urls)),
]
