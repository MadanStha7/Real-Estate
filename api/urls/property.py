from django.urls import include, path
from rest_framework import routers
from property.models import Schedule
from api.viewsets.property_viewset import ScheduleList

from api.viewsets.property_viewset import (
    PropertyViewSet,
    FieldVisitViewSet,
    PropertyDiscussionViewSet,
    RentalViewSet,
    GalleryViewSet,
    AmentitesViewSet,
    ScheduleViewSet,
    LocationViewSet,
    PropertyDetailsView,
    PropertyViewSet,
    FieldVisitViewSet,
    PropertyDiscussionViewSet,
    RentalViewSet,
    GalleryViewSet,
    AmentitesViewSet,
    ScheduleViewSet,
    PropertyList,
    PropertyTop,
    PropertyPremium,
    PropertyFeatured,
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
    path("property-list/", PropertyList.as_view(), name="list_property"),
    path("property-detail/<int:pk>/", PropertyDetailsView.as_view(), name="property_detail"),

    path("property-category/top/", PropertyTop.as_view(), name="property_top"),
    path(
        "property-category/premium/", PropertyPremium.as_view(), name="property_premium"
    ),
    path(
        "property-category/featured/",
        PropertyFeatured.as_view(),
        name="property_featured",
    ),
    # search
]
