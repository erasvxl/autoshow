from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, OrderViewSet, CreatePaymentIntentView, WeatherView

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pay/', CreatePaymentIntentView.as_view(), name='pay'),
    path('weather/', WeatherView.as_view(), name='weather'),
]
