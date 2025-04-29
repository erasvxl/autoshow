from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('client', 'Клиент'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')  # 👈 добавили default

    def is_manager(self):
        return self.role == 'manager'

    def is_client(self):
        return self.role == 'client'

    def is_admin(self):
        return self.role == 'admin'
