from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm
from .models import CustomUser


# 🔐 Проверки по ролям
def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_client(user):
    return user.is_authenticated and user.role == 'client'


# 📝 Регистрация
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # авто-логин после регистрации
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


# 🔐 Вход
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


# 🚪 Выход
def user_logout(request):
    logout(request)
    return redirect("login")


# 👤 Личный кабинет
@login_required
def profile(request):
    return render(request, "users/profile.html")


# 📊 Главная панель в зависимости от роли
@login_required
def dashboard(request):
    user = request.user
    if user.role == 'manager':
        return render(request, 'users/manager_dashboard.html', {'user': user})
    elif user.role == 'admin':
        return render(request, 'users/admin_dashboard.html', {'user': user})
    else:
        return render(request, 'users/client_dashboard.html', {'user': user})


# 📋 Страница, доступная только менеджерам
@user_passes_test(is_manager)
def manager_orders(request):
    from cars.models import CarOrder
    orders = CarOrder.objects.all()
    return render(request, 'users/manager_orders.html', {'orders': orders})


