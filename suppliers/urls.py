from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_list, name='suppliers_list'),
    path('add/', views.add_supplier, name='add_supplier'),
    path('delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),  # на будущее
    path('<int:supplier_id>/add_car/', views.add_car_to_supplier, name='add_car_to_supplier'),
    path('<int:supplier_id>/restock/', views.restock_car, name='restock_car'),

]
