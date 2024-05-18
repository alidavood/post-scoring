from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.blog.views.generic import GenericPostViewSet

app_name = 'blog'

router = DefaultRouter()
router.register(r'generic/posts', GenericPostViewSet, basename='generic-posts')

BLOG_API_V1 = [
    path('', include(router.urls)),

]
