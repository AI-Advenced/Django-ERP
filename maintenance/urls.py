"""
Maintenance & Asset Management URL Configuration
"""

from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    # Dashboard
    path('', views.maintenance_dashboard, name='dashboard'),
    
    # Assets
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/<int:pk>/', views.asset_detail, name='asset_detail'),
    path('assets/create/', views.asset_create, name='asset_create'),
    path('assets/<int:pk>/update/', views.asset_update, name='asset_update'),
    path('assets/<int:pk>/delete/', views.asset_delete, name='asset_delete'),
    
    # Preventive Maintenance
    path('preventive-maintenance/', views.pm_list, name='pm_list'),
    path('preventive-maintenance/<int:pk>/', views.pm_detail, name='pm_detail'),
    path('preventive-maintenance/create/', views.pm_create, name='pm_create'),
    path('preventive-maintenance/<int:pk>/update/', views.pm_update, name='pm_update'),
    path('preventive-maintenance/<int:pk>/delete/', views.pm_delete, name='pm_delete'),
    
    # Work Orders
    path('work-orders/', views.workorder_list, name='workorder_list'),
    path('work-orders/<int:pk>/', views.workorder_detail, name='workorder_detail'),
    path('work-orders/create/', views.workorder_create, name='workorder_create'),
    path('work-orders/<int:pk>/update/', views.workorder_update, name='workorder_update'),
    path('work-orders/<int:pk>/delete/', views.workorder_delete, name='workorder_delete'),
    
    # Maintenance Logs
    path('logs/', views.log_list, name='log_list'),
    path('logs/create/', views.log_create, name='log_create'),
]
