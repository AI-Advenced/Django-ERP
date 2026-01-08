from django.urls import path
from . import views

app_name = 'financial'

urlpatterns = [
    # Dashboard
    path('', views.financial_dashboard, name='dashboard'),
    
    # Accounts
    path('accounts/', views.AccountListView.as_view(), name='account_list'),
    path('accounts/create/', views.AccountCreateView.as_view(), name='account_create'),
    path('accounts/<int:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('accounts/<int:pk>/update/', views.AccountUpdateView.as_view(), name='account_update'),
    path('accounts/<int:pk>/delete/', views.AccountDeleteView.as_view(), name='account_delete'),
    
    # Customers
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    
    # Invoices
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/create/', views.InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<int:pk>/update/', views.InvoiceUpdateView.as_view(), name='invoice_update'),
    path('invoices/<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='invoice_delete'),
    
    # Bills
    path('bills/', views.BillListView.as_view(), name='bill_list'),
    path('bills/create/', views.BillCreateView.as_view(), name='bill_create'),
    path('bills/<int:pk>/', views.BillDetailView.as_view(), name='bill_detail'),
    path('bills/<int:pk>/update/', views.BillUpdateView.as_view(), name='bill_update'),
    path('bills/<int:pk>/delete/', views.BillDeleteView.as_view(), name='bill_delete'),
    
    # Payments
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/create/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('payments/<int:pk>/update/', views.PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment_delete'),
    
    # Expenses
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/create/', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/<int:pk>/update/', views.ExpenseUpdateView.as_view(), name='expense_update'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense_delete'),
    
    # Journal Entries
    path('journal-entries/', views.JournalEntryListView.as_view(), name='journal_entry_list'),
    path('journal-entries/create/', views.JournalEntryCreateView.as_view(), name='journal_entry_create'),
    path('journal-entries/<int:pk>/', views.JournalEntryDetailView.as_view(), name='journal_entry_detail'),
    path('journal-entries/<int:pk>/update/', views.JournalEntryUpdateView.as_view(), name='journal_entry_update'),
    path('journal-entries/<int:pk>/delete/', views.JournalEntryDeleteView.as_view(), name='journal_entry_delete'),
    
    # Budgets
    path('budgets/', views.BudgetListView.as_view(), name='budget_list'),
    path('budgets/create/', views.BudgetCreateView.as_view(), name='budget_create'),
    path('budgets/<int:pk>/', views.BudgetDetailView.as_view(), name='budget_detail'),
    path('budgets/<int:pk>/update/', views.BudgetUpdateView.as_view(), name='budget_update'),
    path('budgets/<int:pk>/delete/', views.BudgetDeleteView.as_view(), name='budget_delete'),
]
