from django import forms
from .models import (
    Supplier, PurchaseRequisition, PurchaseRequisitionItem,
    PurchaseOrder, PurchaseOrderItem, GoodsReceipt, GoodsReceiptItem,
    RFQ, RFQItem, SupplierQuotation
)


class SupplierForm(forms.ModelForm):
    """Form for creating and updating suppliers."""
    
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if Supplier.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A supplier with this email already exists.')
        return email
    
    def clean_credit_limit(self):
        """Validate credit limit is non-negative."""
        credit_limit = self.cleaned_data.get('credit_limit')
        if credit_limit < 0:
            raise forms.ValidationError('Credit limit cannot be negative.')
        return credit_limit


class PurchaseRequisitionForm(forms.ModelForm):
    """Form for creating and updating purchase requisitions."""
    
    class Meta:
        model = PurchaseRequisition
        fields = [
            'requisition_number', 'title', 'requested_by', 'department',
            'requisition_date', 'required_by_date', 'priority', 'purpose', 'notes'
        ]
        widgets = {
            'requisition_date': forms.DateInput(attrs={'type': 'date'}),
            'required_by_date': forms.DateInput(attrs={'type': 'date'}),
            'purpose': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        """Validate dates."""
        cleaned_data = super().clean()
        requisition_date = cleaned_data.get('requisition_date')
        required_by_date = cleaned_data.get('required_by_date')
        
        if requisition_date and required_by_date:
            if required_by_date < requisition_date:
                raise forms.ValidationError('Required by date cannot be before requisition date.')
        
        return cleaned_data


class PurchaseOrderForm(forms.ModelForm):
    """Form for creating and updating purchase orders."""
    
    class Meta:
        model = PurchaseOrder
        fields = [
            'po_number', 'supplier', 'requisition', 'po_date', 'expected_delivery_date',
            'delivery_address', 'delivery_contact', 'delivery_phone',
            'payment_terms', 'notes', 'supplier_notes', 'terms_conditions', 'created_by'
        ]
        widgets = {
            'po_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'supplier_notes': forms.Textarea(attrs={'rows': 3}),
            'terms_conditions': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean(self):
        """Validate dates."""
        cleaned_data = super().clean()
        po_date = cleaned_data.get('po_date')
        expected_delivery_date = cleaned_data.get('expected_delivery_date')
        
        if po_date and expected_delivery_date:
            if expected_delivery_date < po_date:
                raise forms.ValidationError('Expected delivery date cannot be before PO date.')
        
        return cleaned_data


class GoodsReceiptForm(forms.ModelForm):
    """Form for creating and updating goods receipts."""
    
    class Meta:
        model = GoodsReceipt
        fields = [
            'grn_number', 'purchase_order', 'receipt_date', 'received_by',
            'delivery_note_number', 'vehicle_number', 'driver_name', 'notes'
        ]
        widgets = {
            'receipt_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class RFQForm(forms.ModelForm):
    """Form for creating and updating RFQs."""
    
    class Meta:
        model = RFQ
        fields = [
            'rfq_number', 'title', 'requisition', 'rfq_date', 'submission_deadline',
            'description', 'terms_conditions', 'notes', 'created_by'
        ]
        widgets = {
            'rfq_date': forms.DateInput(attrs={'type': 'date'}),
            'submission_deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'terms_conditions': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        """Validate dates."""
        cleaned_data = super().clean()
        rfq_date = cleaned_data.get('rfq_date')
        submission_deadline = cleaned_data.get('submission_deadline')
        
        if rfq_date and submission_deadline:
            if submission_deadline < rfq_date:
                raise forms.ValidationError('Submission deadline cannot be before RFQ date.')
        
        return cleaned_data


class SupplierQuotationForm(forms.ModelForm):
    """Form for creating and updating supplier quotations."""
    
    class Meta:
        model = SupplierQuotation
        fields = [
            'quotation_number', 'rfq', 'supplier', 'quotation_date', 'valid_until',
            'payment_terms', 'delivery_time', 'notes', 'evaluation_notes', 'evaluation_score'
        ]
        widgets = {
            'quotation_date': forms.DateInput(attrs={'type': 'date'}),
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'evaluation_notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        """Validate dates and scores."""
        cleaned_data = super().clean()
        quotation_date = cleaned_data.get('quotation_date')
        valid_until = cleaned_data.get('valid_until')
        evaluation_score = cleaned_data.get('evaluation_score')
        
        if quotation_date and valid_until:
            if valid_until < quotation_date:
                raise forms.ValidationError('Valid until date cannot be before quotation date.')
        
        if evaluation_score and (evaluation_score < 0 or evaluation_score > 100):
            raise forms.ValidationError('Evaluation score must be between 0 and 100.')
        
        return cleaned_data
