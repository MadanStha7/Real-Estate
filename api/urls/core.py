from django.urls import include, path
from api.urls.user import urlpatterns as user_routes
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += user_routes
