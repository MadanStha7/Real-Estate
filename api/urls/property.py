from django.urls import include, path
from rest_framework import routers
from property.models import BasicDetails
from api.viewsets.property_viewset import (
    BasicDetailsViewset,
    CityViewset,
    PropertyTypesViewSet,
    PropertyCategoryViewset,
    SellPropertyDetailsViewSet,
    ResaleDetailsViewSet,
    AmenitiesViewSet
)

router = routers.DefaultRouter()
router.register(r"city", CityViewset)
router.register(r"property-types", PropertyTypesViewSet)
router.register(r"property-category", PropertyCategoryViewset)
router.register(r"basic-details", BasicDetailsViewset)
router.register(r"sell-property-details", SellPropertyDetailsViewSet)
router.register(r"resale-details", ResaleDetailsViewSet)
router.register(r"sell-amenities", AmenitiesViewSet)



urlpatterns = [
    path("", include(router.urls)),
    # path("admin_dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
]
