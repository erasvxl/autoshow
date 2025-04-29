from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name
