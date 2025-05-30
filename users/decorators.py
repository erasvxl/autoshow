from django.http import HttpResponseForbidden

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.role != role:
                return HttpResponseForbidden("У вас нет доступа к этой странице.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
