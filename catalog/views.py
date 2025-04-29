from rest_framework import viewsets
from .models import Car, Order
from .serializers import CarSerializer, OrderSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import stripe, requests
from .tasks import send_telegram_message

stripe.api_key = settings.STRIPE_SECRET_KEY


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        print(">> [VIEW] perform_create: order создан, делаем .delay()")
        send_telegram_message.delay(
            f"🆕 Новый заказ #{order.id} от пользователя {order.user.username}"
        )


class CreatePaymentIntentView(APIView):
    def post(self, request):
        intent = stripe.PaymentIntent.create(
            amount=10000,
            currency='usd',
            metadata={'order_id': 1}
        )
        return Response({'client_secret': intent.client_secret})


class WeatherView(APIView):
    def get(self, request):
        city = request.GET.get('city', 'Moscow')
        api_key = 'your_openweather_api_key'
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        return Response(response.json())
