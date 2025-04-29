from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from .forms import CarForm, CarFilterForm, CarBrandForm
from .utils import get_car_models
from users.utils import is_staff_user
from django.contrib.auth.decorators import user_passes_test
from users.utils import is_manager_or_admin

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})

@user_passes_test(is_staff_user)
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'cars/car_form.html', {'form': form})

@user_passes_test(is_staff_user)
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/car_form.html', {'form': form})

@user_passes_test(is_staff_user)
def car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'cars/car_confirm_delete.html', {'car': car})


def car_list(request):
    cars = Car.objects.filter(in_stock=True, quantity__gt=0)
    return render(request, 'cars/car_list.html', {'cars': cars})


    if form.is_valid():
        if form.cleaned_data['brand']:
            cars = cars.filter(brand__icontains=form.cleaned_data['brand'])
        if form.cleaned_data['min_year']:
            cars = cars.filter(year__gte=form.cleaned_data['min_year'])
        if form.cleaned_data['max_year']:
            cars = cars.filter(year__lte=form.cleaned_data['max_year'])
        if form.cleaned_data['fuel_type']:
            cars = cars.filter(fuel_type=form.cleaned_data['fuel_type'])
        if form.cleaned_data['condition']:
            cars = cars.filter(condition=form.cleaned_data['condition'])

    return render(request, 'cars/car_list.html', {'cars': cars, 'form': form})


from .models import SupplyOrder
from .forms import SupplyOrderForm


def supply_order_list(request):
    orders = SupplyOrder.objects.all()
    return render(request, 'supplies/supply_order_list.html', {'orders': orders})


def supply_order_create(request):
    if request.method == 'POST':
        form = SupplyOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supply_order_list')
    else:
        form = SupplyOrderForm()
    return render(request, 'supplies/supply_order_form.html', {'form': form})


def supply_order_update(request, pk):
    order = get_object_or_404(SupplyOrder, pk=pk)
    if request.method == 'POST':
        form = SupplyOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('supply_order_list')
    else:
        form = SupplyOrderForm(instance=order)
    return render(request, 'supplies/supply_order_form.html', {'form': form})


def supply_order_delete(request, pk):
    order = get_object_or_404(SupplyOrder, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('supply_order_list')
    return render(request, 'supplies/supply_order_confirm_delete.html', {'order': order})


from .forms import DiscountForm


def apply_discount(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.cleaned_data['discount_percentage']
            car.price = car.price * (1 - discount / 100)
            car.save()
            return redirect('car_list')
    else:
        form = DiscountForm()
    return render(request, 'cars/apply_discount.html', {'form': form, 'car': car})


from django.db.models import Sum
from django.shortcuts import render
from .models import Car


def sales_report(request):
    total_sales = Car.objects.filter(condition='sold').aggregate(Sum('price'))['price__sum']
    return render(request, 'reports/sales_report.html', {'total_sales': total_sales})


from .utils import check_vin
from .forms import VINCheckForm


def vin_check(request):
    result = None
    if request.method == 'POST':
        form = VINCheckForm(request.POST)
        if form.is_valid():
            vin = form.cleaned_data['vin']
            result = check_vin(vin)
    else:
        form = VINCheckForm()
    return render(request, 'cars/vin_check.html', {'form': form, 'result': result})


def car_models(request):
    models = []
    if request.method == 'POST':
        form = CarBrandForm(request.POST)
        if form.is_valid():
            brand = form.cleaned_data['brand']
            models = get_car_models(brand)
    else:
        form = CarBrandForm()
    return render(request, 'cars/car_models.html', {'form': form, 'models': models})


from django.shortcuts import render, get_object_or_404
from .models import Car


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car': car})


from django import forms
from .models import Car


class CarFilterForm(forms.Form):
    brand = forms.CharField(required=False, label="Марка")
    min_year = forms.IntegerField(required=False, label="От года")
    max_year = forms.IntegerField(required=False, label="До года")
    fuel_type = forms.ChoiceField(choices=[('', 'Любой')] + list(Car.FUEL_TYPES), required=False, label="Тип топлива")
    condition = forms.ChoiceField(choices=[('', 'Любое')] + list(Car.CONDITION_TYPES), required=False,
                                  label="Состояние")




from .models import Car, CarOrder
from .forms import CarOrderForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from catalog.tasks import send_telegram_message
@login_required
def order_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, in_stock=True)

    # Проверка доступности машины
    if car.quantity <= 0:
        return redirect('car_list')  # или покажи сообщение "Нет в наличии"

    if request.method == 'POST':
        form = CarOrderForm(request.POST)
        if form.is_valid():
            # Создание заказа
            order = form.save(commit=False)
            order.user = request.user
            order.car = car
            order.save()

            # Уменьшаем количество после успешного заказа
            car.quantity -= 1
            car.save()

            # Отправка уведомления в Telegram
            send_telegram_message.delay(
                f"🆕 Новый заказ машины #{order.id} от пользователя {order.user.username}"
            )

            return redirect('my_orders')
    else:
        form = CarOrderForm()

    return render(request, 'cars/order_form.html', {'form': form, 'car': car})


@login_required
def my_orders(request):
    orders = CarOrder.objects.filter(user=request.user).select_related('car')
    return render(request, 'cars/my_orders.html', {'orders': orders})

@user_passes_test(is_manager_or_admin)
def approve_order(request, order_id):
    order = get_object_or_404(CarOrder, id=order_id)
    order.status = 'approved'
    order.save()
    return redirect('all_orders')

@user_passes_test(is_manager_or_admin)
def reject_order(request, order_id):
    order = get_object_or_404(CarOrder, id=order_id)
    order.status = 'rejected'
    order.save()
    return redirect('all_orders')
@user_passes_test(is_manager_or_admin)
def all_orders(request):
    orders = CarOrder.objects.filter(status='pending').select_related('car', 'user')
    return render(request, 'cars/all_orders.html', {'orders': orders})