from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Car(models.Model):
    name = models.CharField("Название", max_length=100)
    brand = models.CharField("Марка", max_length=50)
    model = models.CharField("Модель", max_length=50, default="Не указана")
    color = models.CharField("Цвет", max_length=30, default="Черный")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    year = models.PositiveIntegerField("Год выпуска", default=2024)
    image = models.ImageField("Изображение", upload_to='cars/', null=True, blank=True)
    is_available = models.BooleanField("В наличии", default=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"



class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('paid', 'Оплачен'),
        ('canceled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Машина")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"Заказ #{self.id} — {self.car.name} — {self.get_status_display()}"
