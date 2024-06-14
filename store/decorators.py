from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        request.is_admin = request.user.is_superuser
        return view_func(request, *args, **kwargs)
    return _wrapped_view
