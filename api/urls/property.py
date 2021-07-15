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
    PropertyFilter,
    PropertyRequestViewSet,
    PropertyDiscussionViewSet,
    ListedPropertyViewSet,
    AssignPropertyRequestViewset,
    PremiumPropetyViewSet,
    FeaturedPropetyViewSet,
    FreePropetyViewSet,
    PropertySearchViewSet,
    DashBoardPendingPropertyView,
    BasicDetailRetrieveView,
    FloorPlanViewset,
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
# sale
router.register(r"sell-property-details", SellPropertyDetailsViewSet)
router.register(r"resale-details", ResaleDetailsViewSet)
router.register(r"sell-amenities", AmenitiesViewSet)
router.register(r"property-filter", PropertyFilter)
router.register(r"property-request", PropertyRequestViewSet)
router.register(r"floor-plan", FloorPlanViewset)  # for both sale and rent

urlpatterns = [
    path("", include(router.urls)),
    path("assign-property/", AssignPropertyViewset.as_view()),
    path("assign-property-request/", AssignPropertyRequestViewset.as_view()),
    path("admin_dashboard/", DashBoardView.as_view(), name="admin_dashboard"),
    path("property-free/", FreePropetyViewSet.as_view(), name="free_propety"),
    path(
        "property-featured/", FeaturedPropetyViewSet.as_view(), name="featured_propety"
    ),
    path("property-premium/", PremiumPropetyViewSet.as_view(), name="premium_propety"),
    path("property-search/", PropertySearchViewSet.as_view(), name="search_propety"),
    path(
        "admin-dashboard/pending-property/", DashBoardPendingPropertyView.as_view()
    ),  # admin pending property
    path("basic-details/property/<int:pk>/", BasicDetailRetrieveView.as_view()),
]
