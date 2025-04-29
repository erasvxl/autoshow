from django.db import models
from django.conf import settings  # ВАЖНО: вместо from django.contrib.auth.models import User
from suppliers.models import Supplier

# Автомобиль
class Car(models.Model):
    FUEL_TYPES = [
        ('gasoline', 'Бензин'),
        ('diesel', 'Дизель'),
        ('electric', 'Электро'),
        ('hybrid', 'Гибрид'),
    ]
    CONDITION_TYPES = [
        ('new', 'Новый'),
        ('used', 'Б/у'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    engine_volume = models.DecimalField(max_digits=3, decimal_places=1)
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPES)
    mileage = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=10, choices=CONDITION_TYPES)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, blank=True)

    in_stock = models.BooleanField(default=False)  # машина находится в автосалоне
    quantity = models.PositiveIntegerField(default=0)  # только для машин в салоне

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


# Поставщики
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


# Заказы на поставку
class SupplyOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В пути'),
        ('delivered', 'Доставлено'),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Заказ №{self.id} от {self.supplier.name} ({self.get_status_display()})"


# История изменения цен
class PriceHistory(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='price_history')
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car} – {self.old_price} → {self.new_price} ({self.changed_at})"


# Уведомления
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Уведомление для {self.user.username}: {self.message[:30]}..."


# Заказ автомобиля
class CarOrder(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    ]

    COLOR_CHOICES = [
        ('white', 'Белый'),
        ('black', 'Чёрный'),
        ('gray', 'Серый'),
        ('red', 'Красный'),
        ('blue', 'Синий'),
    ]

    COMPLETION_CHOICES = [
        ('standard', 'Стандарт'),
        ('comfort', 'Комфорт'),
        ('luxury', 'Люкс'),
    ]
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('approved', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    ]
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    completion = models.CharField(max_length=20, choices=COMPLETION_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    pickup_date = models.DateField()
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.car}"

