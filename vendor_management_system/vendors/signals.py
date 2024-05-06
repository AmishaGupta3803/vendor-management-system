from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .utils import calculate_vendor_performance_metrics

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics_on_po_save(sender, instance, created, **kwargs):
    if created or instance.status == 'completed' or instance.quality_rating or instance.acknowledgment_date:
        calculate_vendor_performance_metrics(instance.vendor)

        # Update historical performance
        HistoricalPerformance.objects.create(
            vendor=instance.vendor,
            on_time_delivery_rate=instance.vendor.on_time_delivery_rate,
            quality_rating_avg=instance.vendor.quality_rating_avg,
            average_response_time=instance.vendor.average_response_time,
            fulfillment_rate=instance.vendor.fulfillment_rate
        )

@receiver(pre_delete, sender=PurchaseOrder)
def update_vendor_performance_metrics_on_po_delete(sender, instance, **kwargs):
    calculate_vendor_performance_metrics(instance.vendor)

    # Update historical performance
    HistoricalPerformance.objects.create(
        vendor=instance.vendor,
        on_time_delivery_rate=instance.vendor.on_time_delivery_rate,
        quality_rating_avg=instance.vendor.quality_rating_avg,
        average_response_time=instance.vendor.average_response_time,
        fulfillment_rate=instance.vendor.fulfillment_rate
    )
