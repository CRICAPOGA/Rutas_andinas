from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('home')  # No autenticado va al home

            user_role = getattr(request.user.role_id, 'role', None)

            if user_role not in allowed_roles:
                return redirect('home')  # Rol no permitido va al home

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator