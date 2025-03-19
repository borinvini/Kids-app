from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ChildViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'children', ChildViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
]