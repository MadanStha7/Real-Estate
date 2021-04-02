from django.urls import include, path
from api.urls.user import urlpatterns as user_routes
from api.urls.property import  urlpatterns as property_routes
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += user_routes
urlpatterns += property_routes
# urlpatterns += serviceprovider_routes
# urlpatterns += property_service_routes
