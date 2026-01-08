from django.urls import path
from . import views

app_name = 'fiscal'

urlpatterns = [
    # TaxRate URLs
    path('taxrates/', views.TaxRateListView.as_view(), name='taxrate_list'),
    path('taxrates/create/', views.TaxRateCreateView.as_view(), name='taxrate_create'),
    path('taxrates/<int:pk>/', views.TaxRateDetailView.as_view(), name='taxrate_detail'),
    path('taxrates/<int:pk>/update/', views.TaxRateUpdateView.as_view(), name='taxrate_update'),
    path('taxrates/<int:pk>/delete/', views.TaxRateDeleteView.as_view(), name='taxrate_delete'),
    
    # FiscalYear URLs
    path('fiscal-years/', views.FiscalYearListView.as_view(), name='fiscalyear_list'),
    path('fiscal-years/create/', views.FiscalYearCreateView.as_view(), name='fiscalyear_create'),
    path('fiscal-years/<int:pk>/', views.FiscalYearDetailView.as_view(), name='fiscalyear_detail'),
    path('fiscal-years/<int:pk>/update/', views.FiscalYearUpdateView.as_view(), name='fiscalyear_update'),
    path('fiscal-years/<int:pk>/delete/', views.FiscalYearDeleteView.as_view(), name='fiscalyear_delete'),
    
    # Invoice URLs
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/create/', views.InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<int:pk>/update/', views.InvoiceUpdateView.as_view(), name='invoice_update'),
    path('invoices/<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='invoice_delete'),
    
    # Payment URLs
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/create/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment_delete'),
    
    # TaxReport URLs
    path('tax-reports/', views.TaxReportListView.as_view(), name='taxreport_list'),
    path('tax-reports/create/', views.TaxReportCreateView.as_view(), name='taxreport_create'),
    path('tax-reports/<int:pk>/', views.TaxReportDetailView.as_view(), name='taxreport_detail'),
    path('tax-reports/<int:pk>/update/', views.TaxReportUpdateView.as_view(), name='taxreport_update'),
    path('tax-reports/<int:pk>/delete/', views.TaxReportDeleteView.as_view(), name='taxreport_delete'),
]
