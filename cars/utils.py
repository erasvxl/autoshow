from django.core.mail import send_mail
from django.contrib.auth.models import User

def notify_users(subject, message):
    users = User.objects.all()
    recipient_list = [user.email for user in users if user.email]
    send_mail(subject, message, 'noreply@autoshop.com', recipient_list, fail_silently=True)


import requests


def check_vin(vin):
    api_key = "your_api_key"
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['Results']
    return None
def get_car_models(brand):
    url = f"https://www.carqueryapi.com/api/0.3/?cmd=getModels&make={brand}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('Models', [])
    return []
