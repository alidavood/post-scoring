from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.generic import UserViewSet

app_name = 'user'

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user_profile')

USER_API_V1 = [
    path('', include(router.urls)),
]
