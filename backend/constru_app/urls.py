from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/token/', obtain_auth_token, name='api-token-auth'),
    path(
        'api/schema/',
        SpectacularAPIView.as_view(authentication_classes=[], permission_classes=[]),
        name='api-schema',
    ),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema', authentication_classes=[], permission_classes=[]),
        name='api-docs',
    ),
    path('api/', include('projects.urls')),
]
