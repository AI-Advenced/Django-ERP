"""
Quality Management URL Configuration
"""

from django.urls import path
from . import views

app_name = 'quality'

urlpatterns = [
    # Dashboard
    path('', views.quality_dashboard, name='dashboard'),
    
    # Inspections
    path('inspections/', views.inspection_list, name='inspection_list'),
    path('inspections/<int:pk>/', views.inspection_detail, name='inspection_detail'),
    path('inspections/create/', views.inspection_create, name='inspection_create'),
    path('inspections/<int:pk>/update/', views.inspection_update, name='inspection_update'),
    path('inspections/<int:pk>/delete/', views.inspection_delete, name='inspection_delete'),
    
    # Non-Conformance Reports
    path('ncr/', views.nonconformance_list, name='nonconformance_list'),
    path('ncr/<int:pk>/', views.nonconformance_detail, name='nonconformance_detail'),
    path('ncr/create/', views.nonconformance_create, name='nonconformance_create'),
    path('ncr/<int:pk>/update/', views.nonconformance_update, name='nonconformance_update'),
    path('ncr/<int:pk>/delete/', views.nonconformance_delete, name='nonconformance_delete'),
    
    # Corrective Actions (CAPA)
    path('capa/', views.capa_list, name='capa_list'),
    path('capa/<int:pk>/', views.capa_detail, name='capa_detail'),
    path('capa/create/', views.capa_create, name='capa_create'),
    path('capa/<int:pk>/update/', views.capa_update, name='capa_update'),
    path('capa/<int:pk>/delete/', views.capa_delete, name='capa_delete'),
]
