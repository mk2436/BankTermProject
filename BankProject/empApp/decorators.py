from django.contrib.auth.decorators import user_passes_test

def role_required(*roles,login_url='/mgr-login/'):
    def decorator(view_func):
        decorated_view_func = user_passes_test(
            lambda user: user.is_authenticated and user.user_type in roles,
            login_url=login_url  
        )(view_func)
        return decorated_view_func
    return decorator