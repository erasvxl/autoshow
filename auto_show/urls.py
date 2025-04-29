from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Auto Show API",
        default_version='v1',
        description="Документация API для автосалона",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),                            # Панель администратора
    path('', include('cars.urls')),                             # Фронтовая часть каталога автомобилей
    path('users/', include('users.urls')),                      # Пользователи

    # API
    path('api/', include('catalog.urls')),                      # REST API: машины, заказы и прочее
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT: вход
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT: обновление

    # Документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('suppliers/', include('suppliers.urls')),

]

# Медиафайлы (изображения авто и т.п.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
