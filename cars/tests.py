from django.test import TestCase
from .models import Car

class CarModelTest(TestCase):
    def setUp(self):
        self.car = Car.objects.create(brand="Toyota", model="Camry", year=2023, price=25000)

    def test_car_creation(self):
        self.assertEqual(self.car.brand, "Toyota")
        self.assertEqual(self.car.year, 2023)

    def test_car_list_view(self):
        response = self.client.get('/cars/')
        self.assertEqual(response.status_code, 200)
