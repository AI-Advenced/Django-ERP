from django.urls import path
from . import views

app_name = 'purchasing'

urlpatterns = [
    # Dashboard
    path('', views.PurchasingDashboardView.as_view(), name='dashboard'),
    
    # Suppliers
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
    
    # Purchase Requisitions
    path('requisitions/', views.RequisitionListView.as_view(), name='requisition_list'),
    path('requisitions/create/', views.RequisitionCreateView.as_view(), name='requisition_create'),
    path('requisitions/<int:pk>/', views.RequisitionDetailView.as_view(), name='requisition_detail'),
    path('requisitions/<int:pk>/edit/', views.RequisitionUpdateView.as_view(), name='requisition_update'),
    path('requisitions/<int:pk>/delete/', views.RequisitionDeleteView.as_view(), name='requisition_delete'),
    
    # Purchase Orders
    path('purchase-orders/', views.PurchaseOrderListView.as_view(), name='purchase_order_list'),
    path('purchase-orders/create/', views.PurchaseOrderCreateView.as_view(), name='purchase_order_create'),
    path('purchase-orders/<int:pk>/', views.PurchaseOrderDetailView.as_view(), name='purchase_order_detail'),
    path('purchase-orders/<int:pk>/edit/', views.PurchaseOrderUpdateView.as_view(), name='purchase_order_update'),
    path('purchase-orders/<int:pk>/delete/', views.PurchaseOrderDeleteView.as_view(), name='purchase_order_delete'),
    
    # Goods Receipts
    path('goods-receipts/', views.GoodsReceiptListView.as_view(), name='goods_receipt_list'),
    path('goods-receipts/create/', views.GoodsReceiptCreateView.as_view(), name='goods_receipt_create'),
    path('goods-receipts/<int:pk>/', views.GoodsReceiptDetailView.as_view(), name='goods_receipt_detail'),
    path('goods-receipts/<int:pk>/edit/', views.GoodsReceiptUpdateView.as_view(), name='goods_receipt_update'),
    path('goods-receipts/<int:pk>/delete/', views.GoodsReceiptDeleteView.as_view(), name='goods_receipt_delete'),
    
    # RFQs
    path('rfqs/', views.RFQListView.as_view(), name='rfq_list'),
    path('rfqs/create/', views.RFQCreateView.as_view(), name='rfq_create'),
    path('rfqs/<int:pk>/', views.RFQDetailView.as_view(), name='rfq_detail'),
    path('rfqs/<int:pk>/edit/', views.RFQUpdateView.as_view(), name='rfq_update'),
    path('rfqs/<int:pk>/delete/', views.RFQDeleteView.as_view(), name='rfq_delete'),
]
