from django.urls import include, path
from rest_framework import routers
from api.viewsets.property_viewset import  PropertyViewSet, \
    GalleryViewSet, FieldVisitViewSet, \
    PropertyDiscussionViewSet, PropertyRequestViewSet

router = routers.DefaultRouter()
router.register(r'property', PropertyViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'field_visits', FieldVisitViewSet)
router.register(r'property_discussion', PropertyDiscussionViewSet)
router.register(r'property_request', PropertyRequestViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
