"""
Signal handlers for Logistics & Supply Chain Management Module
"""
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Inventory, ShipmentItem, StockMovement


@receiver(pre_save, sender=Inventory)
def update_inventory_totals(sender, instance, **kwargs):
    """Update calculated fields before saving inventory"""
    instance.update_totals()


@receiver(pre_save, sender=ShipmentItem)
def calculate_shipment_item_total(sender, instance, **kwargs):
    """Calculate line total before saving shipment item"""
    instance.calculate_line_total()


@receiver(post_save, sender=ShipmentItem)
def update_shipment_total(sender, instance, created, **kwargs):
    """Update shipment total value when items are added/updated"""
    shipment = instance.shipment
    total = sum(item.line_total for item in shipment.items.all())
    if shipment.total_value != total:
        shipment.total_value = total
        shipment.save(update_fields=['total_value'])


@receiver(post_delete, sender=ShipmentItem)
def update_shipment_total_on_delete(sender, instance, **kwargs):
    """Update shipment total when item is deleted"""
    shipment = instance.shipment
    total = sum(item.line_total for item in shipment.items.all())
    if shipment.total_value != total:
        shipment.total_value = total
        shipment.save(update_fields=['total_value'])


@receiver(pre_save, sender=StockMovement)
def calculate_movement_total(sender, instance, **kwargs):
    """Calculate total cost before saving stock movement"""
    instance.calculate_total()


@receiver(post_save, sender=StockMovement)
def update_inventory_on_movement(sender, instance, created, **kwargs):
    """Update inventory quantities when stock movement is created"""
    if created and instance.inventory:
        inventory = instance.inventory
        
        # Update quantity based on movement type
        if instance.movement_type in ['receipt', 'return']:
            # Positive movements - increase stock
            inventory.quantity_on_hand += abs(instance.quantity)
        elif instance.movement_type in ['issue', 'scrap']:
            # Negative movements - decrease stock
            inventory.quantity_on_hand -= abs(instance.quantity)
        elif instance.movement_type == 'adjustment':
            # Adjustment - can be positive or negative
            inventory.quantity_on_hand += instance.quantity
        
        # Recalculate available quantity and total value
        inventory.update_totals()
        inventory.save()
