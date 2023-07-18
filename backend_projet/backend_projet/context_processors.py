def custom_context(request):
    # Vos variables de contexte personnalisées
    custom_variable = "Valeur personnalisée"


    context = locals()
    # Retourne un dictionnaire contenant les variables de contexte
    return context