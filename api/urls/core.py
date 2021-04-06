from django.urls import include, path
from api.urls.user import urlpatterns as user_routes
from api.urls.property import  urlpatterns as property_routes
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', include_docs_urls(title='API Documentation')),
]

urlpatterns += user_routes
urlpatterns += property_routes
# urlpatterns += serviceprovider_routes
# urlpatterns += property_service_routes
