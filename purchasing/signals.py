from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import (
    PurchaseOrderItem, GoodsReceiptItem, PurchaseOrder,
    PurchaseRequisition, PurchaseRequisitionItem
)


@receiver(pre_save, sender=PurchaseOrder)
def calculate_purchase_order_totals(sender, instance, **kwargs):
    """
    Calculate Purchase Order totals before saving.
    """
    if instance.pk:
        # Calculate subtotal from items
        items_total = sum(item.line_total for item in instance.items.all())
        instance.subtotal = items_total
        
        # Calculate tax amount
        instance.tax_amount = instance.subtotal * (instance.tax_rate / 100)
        
        # Calculate total amount
        instance.total_amount = (
            instance.subtotal +
            instance.tax_amount +
            instance.shipping_cost +
            instance.other_charges -
            instance.discount_amount
        )


@receiver(post_save, sender=GoodsReceiptItem)
def update_po_item_received_quantity(sender, instance, **kwargs):
    """
    Update PO item received quantity when goods are received.
    """
    po_item = instance.po_item
    
    # Sum all received quantities for this PO item
    total_received = GoodsReceiptItem.objects.filter(
        po_item=po_item
    ).aggregate(total=sum('quantity_accepted'))['total'] or 0
    
    po_item.quantity_received = total_received
    po_item.save()
    
    # Check if PO is fully received
    purchase_order = po_item.purchase_order
    all_items_received = all(
        item.quantity_received >= item.quantity_ordered
        for item in purchase_order.items.all()
    )
    
    if all_items_received and purchase_order.status != 'received':
        purchase_order.status = 'received'
        purchase_order.save()


@receiver(pre_save, sender=PurchaseRequisition)
def calculate_requisition_totals(sender, instance, **kwargs):
    """
    Calculate Purchase Requisition estimated total before saving.
    """
    if instance.pk:
        items_total = sum(item.estimated_total for item in instance.items.all())
        instance.estimated_total = items_total


@receiver(post_save, sender=PurchaseOrder)
def update_supplier_metrics(sender, instance, created, **kwargs):
    """
    Update supplier metrics when a PO is created or updated.
    """
    supplier = instance.supplier
    
    # Update total orders count
    supplier.total_orders = supplier.purchase_orders.count()
    
    # Update total amount
    supplier.total_amount = supplier.purchase_orders.filter(
        status__in=['sent', 'acknowledged', 'partially_received', 'received', 'closed']
    ).aggregate(total=sum('total_amount'))['total'] or 0
    
    supplier.save()
