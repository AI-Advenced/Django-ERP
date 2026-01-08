from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import SalesOrder, SalesOrderItem, Quotation, QuotationItem


@receiver(post_save, sender=SalesOrderItem)
def update_order_totals(sender, instance, **kwargs):
    """
    Update sales order totals when items are saved
    """
    order = instance.sales_order
    order.calculate_totals()
    order.save()


@receiver(post_save, sender=QuotationItem)
def update_quotation_totals(sender, instance, **kwargs):
    """
    Update quotation totals when items are saved
    """
    quotation = instance.quotation
    quotation.calculate_totals()
    quotation.save()
