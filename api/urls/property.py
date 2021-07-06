from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    # path("admin_dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
]
