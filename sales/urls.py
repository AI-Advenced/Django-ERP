from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Dashboard
    path('', views.SalesDashboardView.as_view(), name='dashboard'),
    
    # Customers
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    
    # Sales Orders
    path('orders/', views.SalesOrderListView.as_view(), name='order_list'),
    path('orders/create/', views.SalesOrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', views.SalesOrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/', views.SalesOrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.SalesOrderDeleteView.as_view(), name='order_delete'),
    
    # Quotations
    path('quotations/', views.QuotationListView.as_view(), name='quotation_list'),
    path('quotations/create/', views.QuotationCreateView.as_view(), name='quotation_create'),
    path('quotations/<int:pk>/', views.QuotationDetailView.as_view(), name='quotation_detail'),
    path('quotations/<int:pk>/update/', views.QuotationUpdateView.as_view(), name='quotation_update'),
    path('quotations/<int:pk>/delete/', views.QuotationDeleteView.as_view(), name='quotation_delete'),
    path('quotations/<int:pk>/convert/', views.convert_quotation_to_order, name='quotation_convert'),
]
