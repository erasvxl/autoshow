from django.urls import path
from . import views

urlpatterns = [
    # Главная
    path('', views.car_list, name='car_list'),

    # Автомобили
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/add/', views.car_create, name='car_create'),
    path('car/edit/<int:pk>/', views.car_update, name='car_edit'),
    path('car/delete/<int:pk>/', views.car_delete, name='car_delete'),

    # Заказы поставок
    path('supplies/', views.supply_order_list, name='supply_order_list'),
    path('supplies/add/', views.supply_order_create, name='supply_order_create'),
    path('supplies/edit/<int:pk>/', views.supply_order_update, name='supply_order_update'),
    path('supplies/delete/<int:pk>/', views.supply_order_delete, name='supply_order_delete'),

    # Прочее
    path('cars/discount/<int:pk>/', views.apply_discount, name='apply_discount'),
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('vin-check/', views.vin_check, name='vin_check'),
    path('car-models/', views.car_models, name='car_models'),

    # 🚗 Заказ машины
    path('order/<int:car_id>/', views.order_car, name='order_car'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('orders/approve/<int:order_id>/', views.approve_order, name='approve_order'),
    path('orders/reject/<int:order_id>/', views.reject_order, name='reject_order'),
    path('all-orders/', views.all_orders, name='all_orders'),

]
