from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from .forms import SupplierForm
from cars.models import Car  # импортируем модель Car
from cars.forms import CarForm  # импортируем форму
from django.contrib.auth.decorators import user_passes_test

def is_manager_or_admin(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name='manager').exists())

@user_passes_test(is_manager_or_admin)
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers})
@user_passes_test(is_manager_or_admin)
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suppliers_list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/add_supplier.html', {'form': form})
@user_passes_test(is_manager_or_admin)
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.delete()
    return redirect('suppliers_list')
@user_passes_test(is_manager_or_admin)
def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    cars = Car.objects.filter(supplier=supplier)

    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        amount = int(request.POST.get('amount', 0))

        car = get_object_or_404(Car, id=car_id)
        car.quantity += amount
        car.save()

        return redirect('supplier_detail', supplier_id=supplier_id)

    return render(request, 'suppliers/supplier_detail.html', {
        'supplier': supplier,
        'cars': cars
    })
@user_passes_test(is_manager_or_admin)
def add_car_to_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.supplier = supplier
            car.save()
            return redirect('supplier_detail', supplier_id=supplier_id)
    else:
        form = CarForm()

    return render(request, 'suppliers/add_car_to_supplier.html', {
        'form': form,
        'supplier': supplier,
    })
@user_passes_test(is_manager_or_admin)
def restock_car(request, supplier_id):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        amount = int(request.POST.get('amount'))

        # Получаем машину у поставщика (без in_stock ограничения)
        supplier_car = get_object_or_404(Car, id=car_id, supplier_id=supplier_id)

        # Ищем машину в автосалоне (в наличии)
        car_in_stock = Car.objects.filter(
            brand=supplier_car.brand,
            model=supplier_car.model,
            year=supplier_car.year,
            in_stock=True
        ).first()

        if car_in_stock:
            # Если уже есть — увеличиваем количество
            car_in_stock.quantity += amount
            car_in_stock.save()
        else:
            # Если нет — создаём копию машины из базы поставщика
            Car.objects.create(
                brand=supplier_car.brand,
                model=supplier_car.model,
                year=supplier_car.year,
                engine_volume=supplier_car.engine_volume,
                fuel_type=supplier_car.fuel_type,
                mileage=supplier_car.mileage,
                price=supplier_car.price,
                condition=supplier_car.condition,
                image=supplier_car.image,
                supplier=supplier_car.supplier,
                quantity=amount,
                in_stock=True
            )

        return redirect('supplier_detail', supplier_id=supplier_id)
