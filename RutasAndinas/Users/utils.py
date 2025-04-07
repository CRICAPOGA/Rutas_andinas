from django.http import HttpResponseForbidden
from functools import wraps

def role_required(allowed_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Debes iniciar sesión.")
            if request.user.role != allowed_role:
                return HttpResponseForbidden("No tienes permisos para acceder a esta vista.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator