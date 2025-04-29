from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Car, PriceHistory, Notification

User = get_user_model()

@receiver(post_save, sender=Car)
def create_price_history(sender, instance, created, **kwargs):
    if created:
        PriceHistory.objects.create(
            car=instance,
            old_price=instance.price,
            new_price=instance.price
        )

@receiver(post_save, sender=Car)
def notify_new_car(sender, instance, created, **kwargs):
    if created and instance.added_by:
        Notification.objects.create(
            user=instance.added_by,
            message=f'Новое авто добавлено: {instance.brand} {instance.model} за ${instance.price}'
        )
