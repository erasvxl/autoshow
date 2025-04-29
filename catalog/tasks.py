from celery import shared_task
import requests
from django.conf import settings
from cars.models import CarOrder
from django.core.files.storage import default_storage

@shared_task
def send_telegram_message(order_id):
    try:
        order = CarOrder.objects.select_related('user', 'car').get(id=order_id)
        user = order.user
        car = order.car

        message = (
            f"🚘 <b>Новый заказ автомобиля</b>\n\n"
            f"👤 <b>Покупатель:</b> {user.username} ({user.email})\n"
            f"🧾 <b>Роль:</b> {user.role}\n\n"
            f"🚗 <b>Модель:</b> {car.brand} {car.model} ({car.year})\n"
            f"⚙️ <b>Комплектация:</b> {order.completion}\n"
            f"🎨 <b>Цвет:</b> {order.color}\n"
            f"🔋 <b>Топливо:</b> {car.fuel_type}\n"
            f"📊 <b>Пробег:</b> {car.mileage} км\n"
            f"💰 <b>Цена:</b> {car.price} USD\n"
            f"💼 <b>Оплата:</b> {order.payment_method}\n"
            f"📆 <b>Дата получения:</b> {order.pickup_date.strftime('%d.%m.%Y')}\n"
            f"⏰ <b>Оформлено:</b> {order.ordered_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"📌 <b>Статус:</b> {order.status.upper()}"
        )

        # Отправка текста
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            data={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML"
            }
        )

        # Отправка фото, если есть
        if car.image:
            photo_path = default_storage.path(car.image.name)
            with open(photo_path, 'rb') as photo:
                requests.post(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendPhoto",
                    data={"chat_id": settings.TELEGRAM_CHAT_ID},
                    files={"photo": photo}
                )

    except Exception as e:
        print(f"❌ Ошибка Telegram уведомления: {e}")
