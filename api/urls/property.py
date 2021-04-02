from django.urls import include, path
from rest_framework import routers
from api.viewsets.property_viewset import PropertyViewSet, \
     FieldVisitViewSet, \
         PropertyDiscussionViewSet,\
             RentalViewSet, \
                 GalleryViewSet, \
                     AmentitesViewSet


router = routers.DefaultRouter()
router.register(r'property', PropertyViewSet)
router.register(r'field_visits', FieldVisitViewSet)
router.register(r'property_discussion', PropertyDiscussionViewSet)
router.register(r'rental',RentalViewSet)
router.register(r'gallery',GalleryViewSet)
router.register(r'amenities', AmentitesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
