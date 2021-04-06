from django.urls import include, path
from rest_framework import routers

from api.views.property_service import PropertyServiceDetailAPIView

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path("property_service/", PropertyServiceDetailAPIView.as_view()),
]