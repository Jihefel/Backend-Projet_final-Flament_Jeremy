from django.shortcuts import redirect
from django.urls import reverse

class AccessRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Restriction d'accès à la page de connexion si l'utilisateur est déjà connecté
        if request.path == reverse('login') and request.user.is_authenticated:
            return redirect('home')  # Rediriger vers la page d'accueil ou une autre page lorsque l'accès est restreint

        # Restriction d'accès au panneau d'administration pour les utilisateurs non connectés ou avec des rôles non autorisés
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_authenticated or request.user.role not in ['admin', 'webmaster', 'stock']:
                return redirect('home')  # Rediriger vers la page d'accueil ou une autre page lorsque l'accès est restreint
        
        response = self.get_response(request)
        return response
