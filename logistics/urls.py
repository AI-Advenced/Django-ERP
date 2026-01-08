"""
URL configuration for Logistics & Supply Chain Management Module
"""
from django.urls import path
from . import views

app_name = 'logistics'

urlpatterns = [
    # Dashboard
    path('', views.logistics_dashboard, name='dashboard'),
    
    # Warehouse URLs
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/create/', views.warehouse_create, name='warehouse_create'),
    path('warehouses/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    path('warehouses/<int:pk>/update/', views.warehouse_update, name='warehouse_update'),
    path('warehouses/<int:pk>/delete/', views.warehouse_delete, name='warehouse_delete'),
    
    # Inventory URLs
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/create/', views.inventory_create, name='inventory_create'),
    path('inventory/<int:pk>/', views.inventory_detail, name='inventory_detail'),
    path('inventory/<int:pk>/update/', views.inventory_update, name='inventory_update'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),
    
    # Shipment URLs
    path('shipments/', views.shipment_list, name='shipment_list'),
    path('shipments/create/', views.shipment_create, name='shipment_create'),
    path('shipments/<int:pk>/', views.shipment_detail, name='shipment_detail'),
    path('shipments/<int:pk>/update/', views.shipment_update, name='shipment_update'),
    path('shipments/<int:pk>/delete/', views.shipment_delete, name='shipment_delete'),
    
    # Route URLs
    path('routes/', views.route_list, name='route_list'),
    path('routes/create/', views.route_create, name='route_create'),
    path('routes/<int:pk>/', views.route_detail, name='route_detail'),
    path('routes/<int:pk>/update/', views.route_update, name='route_update'),
    path('routes/<int:pk>/delete/', views.route_delete, name='route_delete'),
    
    # Delivery URLs
    path('deliveries/', views.delivery_list, name='delivery_list'),
    path('deliveries/create/', views.delivery_create, name='delivery_create'),
    path('deliveries/<int:pk>/', views.delivery_detail, name='delivery_detail'),
    path('deliveries/<int:pk>/update/', views.delivery_update, name='delivery_update'),
    path('deliveries/<int:pk>/delete/', views.delivery_delete, name='delivery_delete'),
    
    # Stock Movement URLs
    path('stock-movements/', views.stock_movement_list, name='stock_movement_list'),
    path('stock-movements/create/', views.stock_movement_create, name='stock_movement_create'),
    path('stock-movements/<int:pk>/', views.stock_movement_detail, name='stock_movement_detail'),
]
