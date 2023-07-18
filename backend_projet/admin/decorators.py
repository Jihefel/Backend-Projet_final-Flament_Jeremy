from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404
from shop.models import User

def admin_required(view_func):
    """
    Decorator pour limiter l'accès aux administrateurs uniquement.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role_id == 1:
            return view_func(request, *args, **kwargs)
        else:
            # Redirection vers une page d'erreur ou une page d'accueil par exemple
            return redirect('error_404')
    
    return wrapper

def admin_or_web_required(view_func):
    """
    Decorator pour limiter l'accès aux administrateurs et webmasters uniquement.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role_id == 1 or request.user.role_id == 3:
            return view_func(request, *args, **kwargs)
        else:
            # Redirection vers une page d'erreur ou une page d'accueil par exemple
            return redirect('error_404')
    
    return wrapper

def admin_or_stock_required(view_func):
    """
    Decorator pour limiter l'accès aux administrateurs et stock uniquement.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role_id == 1 or request.user.role_id == 4:
            return view_func(request, *args, **kwargs)
        else:
            # Redirection vers une page d'erreur ou une page d'accueil par exemple
            return redirect('error_404')
    
    return wrapper


def user_or_admin_required(view_func):
    """
    Decorator pour limiter l'accès à un utilisateur spécifique ou aux administrateurs.
    """
    def wrapper(request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        
        if request.user.is_authenticated and (request.user.id == user_id or request.user.role_id == 1):
            return view_func(request, *args, **kwargs)
        else:
            # Redirection vers une page d'erreur ou une page d'accueil par exemple
            return redirect('error_404')
    
    return wrapper

