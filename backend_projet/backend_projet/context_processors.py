from shop.models import *
from django.db.models import Count


def custom_context(request):
    role_id_admin = 1
    role_id_membre = 2
    role_id_web = 3
    role_id_stock = 4

    is_admin = is_membre = is_web = is_stock = False
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()
        is_web = Roles.objects.filter(id=role_id_web, user=request.user).exists()
        is_stock = Roles.objects.filter(id=role_id_stock, user=request.user).exists()

    # Cart Modal
    products_in_cart = all_products_in_cart = nb_products_in_cart = total_panier = None
    if request.user.is_authenticated:
        products_in_cart = Panier.objects.filter(user=request.user).order_by('-id')[:4]
        all_products_in_cart = Panier.objects.filter(user=request.user)
        nb_products_in_cart = Panier.objects.filter(user=request.user).count()
        total_panier = Panier.get_total_panier(request.user)

    # Infos du site
    infos = InfosQDP.objects.first()

    # Wishlist
    wishlist_products = None
    if request.user.is_authenticated:
        wishlist_products = request.user.produits_wishlist.all()

    # Categories
    categories = Categorie.objects.all()

    # Produits
    products_sorted = Produits.objects.order_by('-date_ajout_produit_db')
    recent_products_sidebar = products_sorted[:4]
    recent_products = products_sorted[:6]
    products_with_comment_count = Produits.objects.annotate(num_comments=Count('commentaire'))
    most_popular_products = products_with_comment_count.order_by('-num_comments')[:6]

    # Blogs
    # Annoter les blogs avec le nombre de commentaires
    # Récupérer les blogs avec le nombre de commentaires
    blogs_with_comment_count = BlogPost.objects.annotate(num_comments=Count('commentaires_lies'))

    # Trier les blogs par nombre de commentaires en ordre décroissant
    most_popular_blogs = blogs_with_comment_count.order_by('-num_comments')[:3]


    # Back
    contacts = Contacts.objects.all()
    unreads = Contacts.objects.filter(lu_par_admin=0)
    nb_unread = unreads.count()
    
    commandes = Commandes.objects.all()
    cmd_unconfirmed = Commandes.objects.filter(statut_commande=0)
    nb_cmd_unconfirmed = cmd_unconfirmed.count()

    blogs = BlogPost.objects.all()
    blogs_unconfirmed = BlogPost.objects.filter(is_confirmed=0)
    nb_blogs_unconfirmed = blogs_unconfirmed.count()

    context = {
        'is_admin': is_admin,
        'is_membre': is_membre,
        'is_web': is_web,
        'is_stock': is_stock,
        'products_in_cart': products_in_cart,
        'all_products_in_cart': all_products_in_cart,
        'nb_products_in_cart': nb_products_in_cart,
        'total_panier': total_panier,
        'infos': infos,
        'wishlist_products': wishlist_products,
        'categories': categories,
        'recent_products_sidebar': recent_products_sidebar,
        'recent_products': recent_products,
        'contacts': contacts,
        'unreads': unreads,
        'nb_unread': nb_unread,
        'commandes': commandes,
        'cmd_unconfirmed': cmd_unconfirmed,
        'nb_cmd_unconfirmed': nb_cmd_unconfirmed,
        'blogs_unconfirmed': blogs_unconfirmed,
        'nb_blogs_unconfirmed': nb_blogs_unconfirmed,
        'most_popular_blogs': most_popular_blogs,
        'most_popular_products': most_popular_products,
    }

    return context
