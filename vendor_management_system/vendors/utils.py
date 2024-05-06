from django.utils import timezone
from .models import Vendor

def calculate_vendor_performance_metrics(vendor):
    # On-Time Delivery Rate
    completed_pos = vendor.purchase_orders.filter(status='completed')
    total_completed_pos = completed_pos.count()
    on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
    if total_completed_pos > 0:
        vendor.on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
    else:
        vendor.on_time_delivery_rate = 0

    # Quality Rating Average
    quality_ratings = completed_pos.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
    if quality_ratings:
        vendor.quality_rating_avg = sum(quality_ratings) / len(quality_ratings)
    else:
        vendor.quality_rating_avg = 0

    # Average Response Time
    response_times = completed_pos.exclude(acknowledgment_date__isnull=True).values_list('acknowledgment_date', 'issue_date')
    response_time_diffs = [(ack_date - issue_date).total_seconds() / 3600 for ack_date, issue_date in response_times]
    if response_time_diffs:
        vendor.average_response_time = sum(response_time_diffs) / len(response_time_diffs)
    else:
        vendor.average_response_time = 0

    # Fulfilment Rate
    fulfilled_pos = completed_pos.filter(status='completed')
    total_pos = vendor.purchase_orders.count()
    if total_pos > 0:
        vendor.fulfillment_rate = (fulfilled_pos.count() / total_pos) * 100
    else:
        vendor.fulfillment_rate = 0

    vendor.save()
