from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('manager-orders/', views.manager_orders, name='manager_orders'),
]
