from django.core.exceptions import PermissionDenied

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

def is_staff_user(user):  # 👨‍💼 Менеджер или Админ
    return user.is_authenticated and user.role in ['manager', 'admin']
def is_manager_or_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.role == 'manager')
