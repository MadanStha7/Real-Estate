from django.urls import include, path
from rest_framework import routers
from property.models import Schedule
from api.viewsets.property_viewset import ScheduleList

from api.viewsets.property_viewset import PropertyViewSet, \
     FieldVisitViewSet, \
         PropertyDiscussionViewSet,\
             RentalViewSet, \
                 GalleryViewSet, \
                     AmentitesViewSet,ScheduleViewSet
from api.viewsets.property_viewset import (
    PropertyViewSet,
    FieldVisitViewSet,
    PropertyDiscussionViewSet,
    RentalViewSet,
    GalleryViewSet,
    AmentitesViewSet,
    ScheduleViewSet,
    LocationViewSet,
)


router = routers.DefaultRouter()
router.register(r"property", PropertyViewSet)
router.register(r"location", LocationViewSet)
router.register(r"field_visits", FieldVisitViewSet)
router.register(r"property_discussion", PropertyDiscussionViewSet)
router.register(r"rental", RentalViewSet)
router.register(r"gallery", GalleryViewSet)
router.register(r"amenities", AmentitesViewSet)
router.register(r"schedule", ScheduleViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
