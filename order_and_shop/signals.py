from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .tools import send_order_to_external_api


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    if instance.status == 'complete' and instance.shop.status == 'open':
        try:
            send_order_to_external_api(instance.order_id, instance.shop.id)
        except Exception as e:
            print(f"Failed to send order {instance.order_id} to external API: {e}")
