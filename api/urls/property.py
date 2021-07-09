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
    GalleryViewset,
    PendingPropertyViewset,
    AssignPropertyViewset,
    SellPropertyDetailsViewSet,
    ResaleDetailsViewSet,
    LocalityViewset,
    AmenitiesViewSet,
    FieldVisitViewSet,
    DashBoardView,
    GalleryImageUploadViewset,
    PropertyFilter,
    PropertyRequestViewSet,
    PropertyDiscussionViewSet,
    ListedPropertyViewSet
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
router.register(r"property-discussion", PropertyDiscussionViewSet)
# router.register(r"locality-details", LocalityDetailsViewset)
# rent
router.register(r"rental-details", RentalDetailsViewset)
router.register(r"gallery", GalleryViewset)
router.register(r"pending-property", PendingPropertyViewset)  # pending property
router.register(r"listed-property", ListedPropertyViewSet)  # listed property
router.register(
    r"rent-gallery-image-upload", GalleryImageUploadViewset
)  # pending property

# router.register(r"assign-property", AssignPropertyViewset)  # pending property
# sale
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
