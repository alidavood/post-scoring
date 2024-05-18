from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.user.urls import USER_API_V1
from apps.blog.urls import BLOG_API_V1

API_V1 = settings.API_V1_PREFIX
schema_view = get_schema_view(
    openapi.Info(
        title="Blog Scoring Backend API",
        default_version='V1',
        description="""Project name: Blog Scoring Service""",
        terms_of_service="http://blog-scoring-service.example/",
        contact=openapi.Contact(email="alidavood.it@gmail.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

swagger_urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
    path('', include(swagger_urlpatterns)),
    path('admin/', admin.site.urls),
    path(f'{API_V1}/users/', include(USER_API_V1)),
    path(f'{API_V1}/blog/', include(BLOG_API_V1)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
