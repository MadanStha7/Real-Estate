from django.urls import include, path
from rest_framework import routers
from property.models import BasicDetails
from api.viewsets.property_viewset import (
    BasicDetailsViewset,
    CityViewset,
    PropertyTypesViewSet,
    PropertyCategoryViewset,
    RentPropertyDetailsViewset,
    LocalityDetailsViewset,
    RentalDetailsViewset,
    RentGalleryViewset,
    PendingPropertyViewset,
    AssignPropertyViewset,
    SellPropertyDetailsViewSet,
    ResaleDetailsViewSet,
    LocalityViewset,
    AmenitiesViewSet,
    FieldVisitViewSet,
    DashBoardView,
    PropertyFilter,
    PropertyRequestViewSet
)

router = routers.DefaultRouter()
router.register(r"city", CityViewset)
router.register(r"property-types", PropertyTypesViewSet)
router.register(r"property-category", PropertyCategoryViewset)
router.register(r"basic-details", BasicDetailsViewset)
router.register(r"rent-property-details", RentPropertyDetailsViewset)
router.register(r"locality-details", LocalityDetailsViewset)
router.register(r"locality", LocalityViewset)
router.register(r"field-visit", FieldVisitViewSet)
# router.register(r"locality-details", LocalityDetailsViewset)
router.register(r"rental-details", RentalDetailsViewset)
router.register(r"rent-gallery", RentGalleryViewset)
router.register(r"pending-property", PendingPropertyViewset)  # pending property
# router.register(r"assign-property", AssignPropertyViewset)  # pending property
router.register(r"sell-property-details", SellPropertyDetailsViewSet)
router.register(r"resale-details", ResaleDetailsViewSet)
router.register(r"sell-amenities", AmenitiesViewSet)
router.register(r"property-filter", PropertyFilter)
router.register(r"property-request", PropertyRequestViewSet)



urlpatterns = [
    path("", include(router.urls)),
    path("assign-property/<int:pk>/", AssignPropertyViewset.as_view()),
    path("admin_dashboard/", DashBoardView.as_view(), name="admin_dashboard"),
]
