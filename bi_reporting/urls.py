"""
Business Intelligence & Reporting URL Configuration
"""

from django.urls import path
from . import views

app_name = 'bi_reporting'

urlpatterns = [
    # Main Analytics Dashboard
    path('', views.analytics_dashboard, name='analytics_dashboard'),
    
    # Dashboards
    path('dashboards/', views.dashboard_list, name='dashboard_list'),
    path('dashboards/<int:pk>/', views.dashboard_view, name='dashboard_view'),
    path('dashboards/create/', views.dashboard_create, name='dashboard_create'),
    path('dashboards/<int:pk>/update/', views.dashboard_update, name='dashboard_update'),
    path('dashboards/<int:pk>/delete/', views.dashboard_delete, name='dashboard_delete'),
    
    # KPIs
    path('kpis/', views.kpi_list, name='kpi_list'),
    path('kpis/<int:pk>/', views.kpi_detail, name='kpi_detail'),
    path('kpis/create/', views.kpi_create, name='kpi_create'),
    path('kpis/<int:pk>/update/', views.kpi_update, name='kpi_update'),
    path('kpis/<int:pk>/delete/', views.kpi_delete, name='kpi_delete'),
    
    # Reports
    path('reports/', views.report_list, name='report_list'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<int:pk>/update/', views.report_update, name='report_update'),
    path('reports/<int:pk>/delete/', views.report_delete, name='report_delete'),
    
    # Data Sources
    path('datasources/', views.datasource_list, name='datasource_list'),
    path('datasources/create/', views.datasource_create, name='datasource_create'),
    path('datasources/<int:pk>/update/', views.datasource_update, name='datasource_update'),
    path('datasources/<int:pk>/delete/', views.datasource_delete, name='datasource_delete'),
]
