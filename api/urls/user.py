from django.urls import include, path
from rest_framework import router
from user import views


router = router.DefaultRouter()
router.register(r'usersprofile'
                ,views.UserProfileViewSet)
router.register(r'agentdetail',views.AgentDetailViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]