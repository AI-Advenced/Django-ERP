"""
Forms for Logistics & Supply Chain Management Module
"""
from django import forms
from .models import (
    Warehouse, Inventory, Shipment, ShipmentItem, 
    Route, Delivery, StockMovement
)


class WarehouseForm(forms.ModelForm):
    """Form for creating and updating warehouses"""
    
    class Meta:
        model = Warehouse
        fields = [
            'code', 'name', 'warehouse_type', 'address', 'city', 'state',
            'country', 'postal_code', 'total_capacity', 'current_utilization',
            'manager_name', 'contact_email', 'contact_phone', 'is_active'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., WH001'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Warehouse name'}),
            'warehouse_type': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'total_capacity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_utilization': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class InventoryForm(forms.ModelForm):
    """Form for managing inventory"""
    
    class Meta:
        model = Inventory
        fields = [
            'warehouse', 'product_code', 'product_name', 'description', 'category',
            'quantity_on_hand', 'quantity_reserved', 'reorder_level', 'reorder_quantity',
            'unit_cost', 'bin_location', 'last_count_date'
        ]
        widgets = {
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU/Product Code'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity_on_hand': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity_reserved': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reorder_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bin_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., A-01-05'}),
            'last_count_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ShipmentForm(forms.ModelForm):
    """Form for creating and updating shipments"""
    
    class Meta:
        model = Shipment
        fields = [
            'shipment_number', 'shipment_type', 'status', 'origin_warehouse',
            'destination_warehouse', 'carrier_name', 'transport_mode', 'tracking_number',
            'scheduled_ship_date', 'actual_ship_date', 'estimated_delivery_date',
            'actual_delivery_date', 'shipping_cost', 'insurance_cost',
            'reference_document', 'notes', 'special_instructions'
        ]
        widgets = {
            'shipment_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SH-XXXX'}),
            'shipment_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'origin_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'destination_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'carrier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'transport_mode': forms.Select(attrs={'class': 'form-select'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control'}),
            'scheduled_ship_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actual_ship_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estimated_delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actual_delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'shipping_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'insurance_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reference_document': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ShipmentItemForm(forms.ModelForm):
    """Form for shipment items"""
    
    class Meta:
        model = ShipmentItem
        fields = [
            'product_code', 'product_name', 'description', 'quantity_shipped',
            'quantity_received', 'unit_of_measure', 'package_count', 'weight',
            'volume', 'unit_price', 'inventory', 'notes'
        ]
        widgets = {
            'product_code': forms.TextInput(attrs={'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'quantity_shipped': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity_received': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit_of_measure': forms.TextInput(attrs={'class': 'form-control'}),
            'package_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'inventory': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class RouteForm(forms.ModelForm):
    """Form for creating and updating routes"""
    
    class Meta:
        model = Route
        fields = [
            'route_code', 'route_name', 'status', 'start_warehouse',
            'description', 'total_distance', 'estimated_duration',
            'estimated_cost', 'frequency'
        ]
        widgets = {
            'route_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RT-XXXX'}),
            'route_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'start_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'total_distance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estimated_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DeliveryForm(forms.ModelForm):
    """Form for creating and updating deliveries"""
    
    class Meta:
        model = Delivery
        fields = [
            'delivery_number', 'route', 'shipment', 'status', 'delivery_address',
            'delivery_contact', 'delivery_phone', 'scheduled_date',
            'actual_start_time', 'actual_end_time', 'driver_name', 'vehicle_number',
            'notes'
        ]
        widgets = {
            'delivery_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DL-XXXX'}),
            'route': forms.Select(attrs={'class': 'form-select'}),
            'shipment': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'delivery_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'actual_start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'actual_end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'driver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class StockMovementForm(forms.ModelForm):
    """Form for recording stock movements"""
    
    class Meta:
        model = StockMovement
        fields = [
            'movement_number', 'movement_type', 'movement_date', 'inventory',
            'quantity', 'unit_of_measure', 'unit_cost', 'reference_document',
            'shipment', 'from_warehouse', 'to_warehouse', 'reason', 'notes',
            'created_by'
        ]
        widgets = {
            'movement_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MV-XXXX'}),
            'movement_type': forms.Select(attrs={'class': 'form-select'}),
            'movement_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'inventory': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit_of_measure': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reference_document': forms.TextInput(attrs={'class': 'form-control'}),
            'shipment': forms.Select(attrs={'class': 'form-select'}),
            'from_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'to_warehouse': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'created_by': forms.TextInput(attrs={'class': 'form-control'}),
        }
