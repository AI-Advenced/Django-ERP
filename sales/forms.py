from django import forms
from .models import Customer, SalesOrder, SalesOrderItem, Quotation, QuotationItem


class CustomerForm(forms.ModelForm):
    """
    Form for creating and editing customers
    """
    class Meta:
        model = Customer
        fields = [
            'name', 'customer_type', 'email', 'phone', 'mobile',
            'address', 'city', 'state', 'country', 'postal_code',
            'company_name', 'tax_id', 'website',
            'credit_limit', 'payment_terms', 'is_active', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'customer_type': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 8900'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 8900'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal/ZIP Code'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name (if applicable)'}),
            'tax_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tax ID/VAT Number'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'credit_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_terms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Days'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }


class SalesOrderForm(forms.ModelForm):
    """
    Form for creating and editing sales orders
    """
    class Meta:
        model = SalesOrder
        fields = [
            'order_number', 'customer', 'order_date', 'expected_delivery_date',
            'status', 'priority', 'subtotal', 'tax_rate', 'tax_amount',
            'discount_percentage', 'discount_amount', 'shipping_cost', 'total_amount', 'paid_amount',
            'shipping_address', 'shipping_city', 'shipping_state', 
            'shipping_country', 'shipping_postal_code',
            'notes', 'terms_conditions', 'internal_notes', 'sales_person'
        ]
        widgets = {
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SO-XXXX'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'order_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '%'}),
            'tax_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '%'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'shipping_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_state': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_country': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Customer-visible notes'}),
            'terms_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Internal use only'}),
            'sales_person': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SalesOrderItemForm(forms.ModelForm):
    """
    Form for sales order items
    """
    class Meta:
        model = SalesOrderItem
        fields = ['product_name', 'product_code', 'description', 'quantity', 
                 'unit_price', 'discount_percentage', 'tax_rate']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU/Code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }


class QuotationForm(forms.ModelForm):
    """
    Form for creating and editing quotations
    """
    class Meta:
        model = Quotation
        fields = [
            'quotation_number', 'customer', 'quotation_date', 'valid_until',
            'status', 'subtotal', 'tax_rate', 'tax_amount', 'discount_amount',
            'total_amount', 'notes', 'terms_conditions', 'sales_person'
        ]
        widgets = {
            'quotation_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'QT-XXXX'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'quotation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valid_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '%'}),
            'tax_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'terms_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sales_person': forms.TextInput(attrs={'class': 'form-control'}),
        }


class QuotationItemForm(forms.ModelForm):
    """
    Form for quotation items
    """
    class Meta:
        model = QuotationItem
        fields = ['product_name', 'product_code', 'description', 'quantity', 
                 'unit_price', 'discount_percentage']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU/Code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }
