
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers, permissions
from api_main.views import PostViewSet, CategoryViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API Documentation",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    ],
)
router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'post', PostViewSet)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), 
        name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), 
        name='schema-redoc'),
    path('api/', include(router.urls)),
    path('graphql/', include('graphql_main.urls')),
    path('', admin.site.urls),
    path('redoc/', include('django.contrib.admindocs.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)