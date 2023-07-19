from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.core.mail import send_mail
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from backend_projet.context_processors import custom_context




def index(request):

    # Partners
    partners = Partenaires.objects.all()

    today = date.today()
    context_global = custom_context(request)

    recent_products = context_global['recent_products']

    if request.user.is_authenticated:
        wishlist_products = request.user.produits_wishlist.all()

    for product in recent_products:
            variants = product.variations.filter(produits=product)
            first_variant = variants.first()
            if first_variant:
                product_variant = ProductVariant.objects.get(product=product, variant=first_variant)
                if product.promo:
                    product_variant.prix_promo = float(product_variant.prix) - (float(product_variant.prix) * (float(product.promo.pourcentage_promo) / 100))
                product.product_variant = product_variant  # Add the product_variant to the product object

    # Section promo
    promos = Promotions.objects.all()[:4]
    all_promos = Promotions.objects.all()
    # Section extra promo
    extra_promo = ExtraPromo.objects.first()
    extra_promo = Promotions.objects.get(extrapromo=extra_promo)


    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 0:
                user_known = User.objects.get(email=email)
                user_known.abonne_newsletter = True
                messages.success(request, f"{user_known.username} successfully subscribed to the newsletter.")
                user_known.save()
            elif User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 1:
                user_known = User.objects.get(email=email)
                messages.warning(request, f"{user_known.username} already subscribed to newsletter.")
            else:
                newsletter_form.save()
                # Envoyer un e-mail de confirmation ou effectuer d'autres actions
                send_mail(
                    "Thanks for subscribing to our newsletter",
                    "",
                    "jfl.jflament@gmail.com",
                    [email],
                    html_message=render_to_string('mails/subscribe_newsletter.html', {'email': email}),
                )
                messages.success(request, "Successfully subscribed to the newsletter.")
            return redirect('home')
    else:
        newsletter_form = NewsletterForm()
    
    context = locals()
    return render(request, 'shop/index.html', context)

def handler404(request, exception=None):
    response = render(request, 'shop/404.html')
    response.status_code = 404
    return response


@login_required(login_url = 'login')
def account(request):
    return render(request, 'shop/my_account.html')

@login_required(login_url = 'login')
def edit_account(request):

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated your profile.")
            return redirect('account')
    else:
        form = EditProfileForm(instance=request.user)
    context = locals()
    return render(request, 'shop/edit_account.html', context)


@login_required(login_url='login')
def direct_newsletter_subscription(request):
    user = User.objects.get(id=request.user.id)
    user.abonne_newsletter = True
    user.save()
    # Envoyer un e-mail de confirmation
    send_mail(
        "Thanks for subscribing to our newsletter",
        "",
        "jfl.jflament@gmail.com",
        [user.email],
        html_message=render_to_string('mails/subscribe_newsletter.html', {'email': user.username}),
    )
    messages.success(request, "Successfully subscribed to the newsletter.")
    return redirect('account')


@login_required(login_url='login')
def my_orders(request):
    # Commandes
    commandes = Commandes.objects.filter(user=request.user).order_by('-id')

    prod_commandes = ProduitsCommandes.objects.all()
    context = locals()
    return render(request, 'shop/my_orders.html', context)



@login_required(login_url='login')
def cart(request):
    context_global = custom_context(request)
    total_panier = context_global['total_panier']

    promo_code_name = "kadri"  # Code promo à appliquer
    promo_code_percentage = 10  # Pourcentage de réduction pour le code promo
    shipping_fee = 4.50
    promo_code_param = request.GET.get('promo_code')  # Récupérer la valeur du champ du code promo depuis la requête

    promo_code_used = request.user.promo_code_used

    if promo_code_used:
        promo_code_param = promo_code_name

    user = request.user

    if promo_code_param:
        if promo_code_param == promo_code_name:
            user.promo_code_used = True
            user.save()
            messages.success(request, f"Promo code '{promo_code_name}' successfully applied")
        else:
            if user.promo_code_used:
                user.promo_code_used = False
                user.save()
            messages.error(request, "Unknown promo code")
    else:
        if user.promo_code_used:
            user.promo_code_used = False
            user.save()
    total_final = Panier.calculate_total_final(total_panier, user)

    
    
    context = locals()
    return render(request, 'shop/cart.html', context)


@login_required(login_url='login')
def remove_promo_code(request):
    user = request.user
    user.promo_code_used = False
    user.save()
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    context_global = custom_context(request)

    nb_products_in_cart = context_global['nb_products_in_cart']
    all_products_in_cart = context_global['all_products_in_cart']
    total_panier = context_global['total_panier']


    if nb_products_in_cart == 0:
        return redirect('all_products')

    promo_code_name = "kadri"  # Code promo à appliquer
    promo_code_percentage = 10  # Pourcentage de réduction pour le code promo
    shipping_fee = 4.50
    total_final = Panier.calculate_total_final(total_panier, request.user)
    total_net = total_final - shipping_fee

    if request.method == "POST":
        commande = Commandes(user=request.user, date_commande=datetime.now(), statut_commande=False, prix_total=total_net)
        commande.save()

        for product in all_products_in_cart:
            produit = get_object_or_404(ProductVariant, id=product.produit_inclus.id)
            produits_commandes = ProduitsCommandes(commande=commande, product_variant=produit, quantite=product.quantite_ajoutee)
            produits_commandes.save()


        user = request.user
        user.promo_code_used = False
        user.save()

        # Ajouter la commande à l'historique de l'user
        request.user.commandes_passees.add(commande)

        # Envoyer un e-mail de confirmation
        send_mail(
            "Confirmation order : pending",
            "",
            "jfl.jflament@gmail.com",
            [request.user.email],
            html_message=render_to_string('mails/order_confirmation.html', {'user': request.user, 'all_products_in_cart': all_products_in_cart, 'total_panier': total_panier, 'promo_code_name': promo_code_name, 'promo_code_percentage': promo_code_percentage, 'shipping_fee': shipping_fee, 'total_final': total_final}),
        )


        # Vider le panier de l'utilisateur
        all_products_in_cart.delete()

        messages.success(request, "Your order has been  successfully submitted and is now pending confirmation. An admin will confirm it when it will be ready. Thank you!")
        return redirect('home')
    
    context = locals()
    return render(request, 'shop/checkout.html', context)


def connection(request):

    if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.username}")
                return redirect('home')
            else:
                if not username in User.objects.all():
                    messages.error(request, "Unknown account.")
                else :
                    messages.error(request, "Username or password incorrect.")
                
                context = locals()
                return render(request, 'shop/login.html', context)
    context = locals()
    return render(request, 'shop/login.html', context)



@login_required(login_url='login')
def deconnection(request):
    logout(request)
    return redirect('home')


@login_required(login_url = 'login')
def change_password(request):

    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=request.user)  # Met à jour la session de l'utilisateur avec le nouveau mot de passe
            messages.success(request, 'Your password has been updated successfully.')
            send_mail(
            f"{user.username}, your password has been changed",
            "",
            "jfl.jflament@gmail.com",
            [user.email],
            html_message=render_to_string('mails/confirm_password.html', {'user': user}),
            )
            return redirect('login')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    context = locals()  
    return render(request, 'shop/change_password.html', context)


def customPasswordReset(request):
    if request.method == 'POST':
        form = CustomResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if not User.objects.filter(email=email).exists():
                messages.error(request, 'Email does not match any known user')
            elif password1 != password2:
                messages.error(request, "Passwords do not match")
            else:
                user = User.objects.get(email=email)
                user.password = make_password(password1)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                send_mail(
                    f"{user.username}, your password has been reset and changed",
                    "",
                    "jfl.jflament@gmail.com",
                    [user.email],
                    html_message=render_to_string('mails/confirm_password.html', {'user': user}),
                    )
                return redirect('login')  # Redirection vers la page de connexion après la modification du mot de passe
    else:
        form = CustomResetPasswordForm()

    context = locals()
    return render(request, 'shop/change_password.html', context)



def all_products(request):
    products = Produits.objects.all()
    today = date.today()
    variants_all = Variantes.objects.all()
    categories = Categorie.objects.all()
    
    if request.GET.get('promotion'):
        promo_param = request.GET.get('promotion')
        if promo_param:
            products = products.filter(promo_id=promo_param)
    
    type_param = request.GET.get('type')
    if request.GET.get('category'):
        # Récupérer les paramètres de filtrage de l'URL
        category_id = int(request.GET.get('category'))

        # Filtrer les catégories en fonction des paramètres
        if category_id:
            products = products.filter(categorie_id=category_id)

    
    # Filtrer par type
    if type_param:
        products = products.filter(type=type_param)
    else:
        type_param = ""

    if request.method == 'GET':
        filter_form = PriceFilterForm(request.GET)
        name_filter = NameFilterForm(request.GET)
        if filter_form.is_valid():
            filter_by_price_max = filter_form.cleaned_data['filter_by_price']
            
            # Filtrer les produits en fonction du prix
            if filter_by_price_max is not None:
                filtered_products = []
                for product in products:
                    variants = product.variations.filter(produits=product)
                    first_variant = variants.first()
                    if first_variant:
                        product_variant = ProductVariant.objects.get(product=product, variant=first_variant)
                        if product_variant.prix <= filter_by_price_max:
                            filtered_products.append(product)
                products = filtered_products
            else:
                filtered_products = products
        if name_filter.is_valid():
            filter_by_name = name_filter.cleaned_data['filter_by_name']
    
            if filter_by_name:
                products = products.filter(nom__icontains=filter_by_name)
                filtered_products = products
            else:
                filtered_products = products
        
    
    products_length = len(products)

    # Vérifier si la liste est vide avant de paginer les produits
    if not filtered_products:
        paginator = Paginator([], 12)
        page_number = 1
        page_obj = paginator.get_page(page_number)
        start_index = 0
        end_index = 0
    else:
        # Pagination des produits
        paginator = Paginator(filtered_products, 12)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Calculate the start and end indexes for the range of products to display
        per_page = 12  # Number of products per page
        start_index = (int(page_number) - 1) * per_page
        end_index = int(page_number) * per_page

        # Adjust end_index if it exceeds the length of the filtered_products list
        end_index = min(end_index, len(filtered_products))

        for product in products:
            variants = product.variations.filter(produits=product)
            first_variant = variants.first()
            if first_variant:
                product_variant = ProductVariant.objects.get(product=product, variant=first_variant)
                if product.promo:
                    product_variant.prix_promo = float(product_variant.prix) - (float(product_variant.prix) * (float(product.promo.pourcentage_promo) / 100))
                product.product_variant = product_variant  # Add the product_variant to the product object
    

    # Slice the products based on the calculated indexes
    sliced_products = products[start_index:end_index]

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 0:
                user_known = User.objects.get(email=email)
                user_known.abonne_newsletter = True
                messages.success(request, f"{user_known.username} successfully subscribed to the newsletter.")
                user_known.save()
            elif User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 1:
                user_known = User.objects.get(email=email)
                messages.warning(request, f"{user_known.username} already subscribed to newsletter.")
            else:
                newsletter_form.save()
                # Envoyer un e-mail de confirmation ou effectuer d'autres actions
                send_mail(
                    "Thanks for subscribing to our newsletter",
                    "",
                    "jfl.jflament@gmail.com",
                    [email],
                    html_message=render_to_string('mails/subscribe_newsletter.html', {'email': email}),
                )
                messages.success(request, "Successfully subscribed to the newsletter.")
            return redirect('home')
    else:
        newsletter_form = NewsletterForm()
    
    context = locals()
    return render(request, 'shop/products-left-sidebar-2.html', context)



def product(request, id):
    
    product = Produits.objects.get(id=id)

    related_products = Produits.objects.all().order_by('?')[:6]

   
    variants = product.variations.filter(produits=product) 

    if request.user.is_authenticated:
        wishlist_products = request.user.produits_wishlist.all()
        wp = wishlist_products.filter(id=product.id)

    if request.GET.get('variant'):
        variant_param = int(request.GET.get('variant'))
        if not variants.filter(id=variant_param).exists():
            return redirect('error_404')
    else:
        if variants.filter(id=1).exists():
            variant_param = 1
        else:
            variant_param = 5

    variant = variants.filter(id=variant_param).first()

    variants_with_stock = []
    for vari in variants:
        product_vari = ProductVariant.objects.get(product=product, variant=vari)
        variant_has_stock = product_vari.quantite_stock > 0
        variant_with_stock = {
            'variant': vari,
            'has_stock': variant_has_stock
        }
        variants_with_stock.append(variant_with_stock)

    if variant:
        product_variant = ProductVariant.objects.get(product=product, variant=variant)
        if product.promo:
            product_variant.prix_promo = float(product_variant.prix) - (float(product_variant.prix) * (float(product.promo.pourcentage_promo) / 100))
        product.product_variant = product_variant  # Add the product_variant to the product object


    for rp in related_products:
        rv = rp.variations.filter(produits=rp).first()
        if rv:
            related_product_variant = ProductVariant.objects.get(product=rp, variant=rv)
            if rp.promo:
                related_product_variant.prix_promo =  float(related_product_variant.prix) - (float(related_product_variant.prix) * (float(rp.promo.pourcentage_promo) / 100))
            rp.related_product_variant = related_product_variant

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 0:
                user_known = User.objects.get(email=email)
                user_known.abonne_newsletter = True
                messages.success(request, f"{user_known.username} successfully subscribed to the newsletter.")
                user_known.save()
            elif User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 1:
                user_known = User.objects.get(email=email)
                messages.warning(request, f"{user_known.username} already subscribed to newsletter.")
            else:
                newsletter_form.save()
                # Envoyer un e-mail de confirmation ou effectuer d'autres actions
                send_mail(
                    "Thanks for subscribing to our newsletter",
                    "",
                    "jfl.jflament@gmail.com",
                    [email],
                    html_message=render_to_string('mails/subscribe_newsletter.html', {'email': email}),
                )
                messages.success(request, "Successfully subscribed to the newsletter.")
            return redirect('home')
    else:
        newsletter_form = NewsletterForm()
    
    context = locals()
    return render(request, 'shop/products-type-1.html', context)

def signup(request):

    if request.method == 'POST':
        form = BootstrapUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.password = make_password(form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            user.save()
            first_user = User.objects.first()
            new_user = User.objects.last()
            if first_user == new_user:
                role = Roles.objects.get(id=1)
                first_user.role = role
                first_user.is_superuser = True
                first_user.is_staff = True
                first_user.save()
            else:
                role = Roles.objects.get(id=2)
                new_user.role = role
                new_user.save()

            return redirect('signup2')

        else:
            if User.objects.filter(email=request.POST['email']).exists():
                messages.error(request, "Email already used.")
            elif User.objects.filter(username=request.POST['username']).exists():
                messages.error(request, "Username already used.")
            else:
                messages.error(request, "Something went wrong.")

    else:
        form = BootstrapUserCreationForm()

    context = locals()
    return render(request, 'shop/signup.html', context)


def signup2(request):
    
    # Form signup 2
    last_user = User.objects.last()
    if request.method == 'POST':
        form = SignupForm2(request.POST, request.FILES, instance=last_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created. Please now log in.")
            user = User.objects.last()
            send_mail(
            f"{user.first_name}, thanks for joining QDP",
            "",
            "jfl.jflament@gmail.com",
            [user.email],
            html_message=render_to_string('mails/account_created.html', {'user': user}),
            )
            return redirect('login')
    else:
        form = SignupForm2()
        newsletter_form = NewsletterForm()

    context = locals()
    return render(request, 'shop/signup2.html', context)

def article(request, id):

    blog = BlogPost.objects.get(id=id)
    cats_blog = CategoriesBlog.objects.all()
    tags = Tags.objects.filter(blogpost=blog)
    all_tags = Tags.objects.all()
    

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 0:
                user_known = User.objects.get(email=email)
                user_known.abonne_newsletter = True
                messages.success(request, f"{user_known.username} successfully subscribed to the newsletter.")
                user_known.save()
            elif User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 1:
                user_known = User.objects.get(email=email)
                messages.warning(request, f"{user_known.username} already subscribed to newsletter.")
            else:
                newsletter_form.save()
                # Envoyer un e-mail de confirmation ou effectuer d'autres actions
                send_mail(
                    "Thanks for subscribing to our newsletter",
                    "",
                    "jfl.jflament@gmail.com",
                    [email],
                    html_message=render_to_string('mails/subscribe_newsletter.html', {'email': email}),
                )
                messages.success(request, "Successfully subscribed to the newsletter.")
            return redirect('home')
    else:
        newsletter_form = NewsletterForm()
    
    context = locals()
    return render(request, 'shop/single-blog-1.html', context)

def blog(request):

    blogs = BlogPost.objects.all().order_by('-date_post')
    cats_blog = CategoriesBlog.objects.all()
    tags = Tags.objects.all()


    if request.GET.get('category_blog'):
        cat_param = request.GET.get('category_blog')
        if cat_param:
            blogs = blogs.filter(categorie_id=cat_param)

    if request.GET.get('tag'):
        tag_param = request.GET.get('tag')
        if tag_param:
            blogs = blogs.filter(tags=tag_param)
    
    if request.method == 'GET':
        filter_by_name = request.GET.get('filter_by_name')

        if filter_by_name:
            blogs = blogs.filter(titre__icontains=filter_by_name)
            filtered_blogs = blogs
        else:
            filtered_blogs = blogs

    # Vérifier si la liste est vide avant de paginer les produits
    if not filtered_blogs:
        paginator = Paginator([], 6)
        page_number = 1
        page_obj = paginator.get_page(page_number)
        start_index = 0
        end_index = 0
    else:
        # Pagination des produits
        paginator = Paginator(blogs, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Calculate the start and end indexes for the range of products to display
        per_page = 6  # Number of products per page
        start_index = (int(page_number) - 1) * per_page
        end_index = int(page_number) * per_page

    # Adjust end_index if it exceeds the length of the filtered_products list
    end_index = min(end_index, len(blogs))

    # Slice the products based on the calculated indexes
    sliced_blogs = blogs[start_index:end_index]

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 0:
                user_known = User.objects.get(email=email)
                user_known.abonne_newsletter = True
                messages.success(request, f"{user_known.username} successfully subscribed to the newsletter.")
                user_known.save()
            elif User.objects.filter(email=email).exists() and User.objects.get(email=email).abonne_newsletter == 1:
                user_known = User.objects.get(email=email)
                messages.warning(request, f"{user_known.username} already subscribed to newsletter.")
            else:
                newsletter_form.save()
                # Envoyer un e-mail de confirmation ou effectuer d'autres actions
                send_mail(
                    "Thanks for subscribing to our newsletter",
                    "",
                    "jfl.jflament@gmail.com",
                    [email],
                    html_message=render_to_string('mails/subscribe_newsletter.html', {'email': email}),
                )
                messages.success(request, "Successfully subscribed to the newsletter.")
            return redirect('home')
    else:
        newsletter_form = NewsletterForm()
    
    context = locals()
    return render(request, 'shop/blog-5.html', context)


@login_required(login_url = 'login')
def wishlist(request, id):
    product = Produits.objects.get(id=id)
    user = request.user

    # Vérifier si le produit est déjà dans la wishlist de l'utilisateur
    if product in user.produits_wishlist.all():
        # Le produit existe déjà, le supprimer de la wishlist
        user.produits_wishlist.remove(product)
        messages.warning(request, f"{product.nom} removed from your wishlist")
    else:
        # Le produit n'existe pas dans la wishlist, l'ajouter
        user.produits_wishlist.add(product)
        messages.success(request, f"{product.nom} added to your wishlist")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def contact(request):


    is_user_authenticated = request.user.is_authenticated
    admins = User.objects.filter(role=1)
    admins_emails = []
    for admin in admins:
        admins_emails.append(admin.email)


    if is_user_authenticated:
        user_auteur = User.objects.get(username=request.user.username)
        initial_values = {'user_auteur': user_auteur}
    else:
        user_auteur = None
        initial_values = {}

    if request.method == 'POST':
        form = ContactForm(request.POST, is_user_authenticated=is_user_authenticated, initial=initial_values)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']

            # Logique pour envoyer le message par email ou effectuer d'autres actions
            if is_user_authenticated:
                # Utilisateur connecté, envoyer un message à l'admin
                messages.success(request, "Message successfully sent to admins")
                contacts = Contacts.objects.create(user_auteur=user_auteur, texte=text)

                # Envoyer un e-mail de confirmation ou effectuer d'autres actions
                send_mail(
                    f"Admins, someone contacted you",
                    "",
                    "jfl.jflament@gmail.com",
                    admins_emails,
                    html_message=render_to_string('mails/contact.html', {'user_auteur': user_auteur, 'text': text}),
                )
                
            else:
                # Utilisateur anonyme, envoyer un message à l'admin par email
                # avec l'adresse email fournie
                messages.success(request, "Message successfully sent to admins")
                contacts = Contacts.objects.create(name=name, email=email, texte=text)

                # Envoyer un e-mail de confirmation ou effectuer d'autres actions
                send_mail(
                    f"Admins, someone contacted you",
                    "",
                    "jfl.jflament@gmail.com",
                    admins_emails,
                    html_message=render_to_string('mails/contact.html', {'name': name, 'email': email, 'text': text}),
                )

            # Redirection vers une page de succès ou une autre action
            return redirect('contact')
    else:
        form = ContactForm(is_user_authenticated=is_user_authenticated, initial=initial_values)

    context = locals()
    return render(request, 'shop/contact.html', context)



# Ajout au panier
@login_required(login_url = 'login')
def add_to_cart(request, id):
    product_variant = ProductVariant.objects.get(id=id)
    product = Produits.objects.get(productvariant=product_variant)
    user = request.user

    # Vérifier si la quantité demandée est valide
    if not request.GET.get('quantity').isdigit() or int(request.GET.get('quantity')) <= 0:
        # Gérer l'erreur de quantité invalide
        messages.error(request,"Invalid quantity")
        return redirect(reverse('product', args=[product.id]) + f"?variant={id}")
    
    quantity = int(request.GET.get('quantity'))

    # Vérifier la disponibilité en stock
    if int(quantity) > product_variant.quantite_stock:
        # Gérer l'erreur de quantité supérieure à la disponibilité en stock
        messages.error(request,"Requested quantity exceeds stock availability")
        return redirect(reverse('product', args=[product.id]) + f"?variant={id}")
    

    # Vérifier si le produit_variant est déjà présent dans le panier de l'utilisateur
    if Panier.objects.filter(produit_inclus_id=product_variant).exists():
        # Si le produit_variant existe déjà, mettre à jour la quantité
        product_in_cart = Panier.objects.get(produit_inclus_id=product_variant)
        product_in_cart.quantite_ajoutee += int(quantity)
        product_in_cart.save()
        product_variant.quantite_stock -= int(quantity)
        product_variant.save()
    else:
        # Si le produit_variant n'existe pas encore, créer une nouvelle entrée dans le panier
        product_in_cart = Panier.objects.create(produit_inclus=product_variant, user=user, quantite_ajoutee=quantity)
        product_variant.quantite_stock -= int(quantity)
        product_variant.save()
    messages.success(request, f"You added {quantity} x {product_variant.variant.contenu} of {product.nom} to your cart")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = 'login')
def update_cart(request):
    all_products_in_cart = Panier.objects.filter(user=request.user)
    promo_code_param = request.POST.get('promo_code')
    
    if request.method == 'POST':
        for product in all_products_in_cart:
            quantity = int(request.POST.get('quantity_' + str(product.id)))
            if quantity <= product.produit_inclus.quantite_stock:
                if quantity == 0:
                    product.delete_from_cart()
                else:
                    product.update_quantity_stock(quantity)

    url = reverse('cart')  # Générer l'URL de la vue 'cart'

    if request.user.promo_code_used:
        promo_code_param = 'kadri'

    if promo_code_param == None:
        url = url
    else:
        url += f'?promo_code={promo_code_param}'  # Ajouter le paramètre promo_code_param à l'URL

    return redirect(url)

@login_required(login_url = 'login')
def delete_from_cart(request,id):
    product_in_cart = Panier.objects.get(produit_inclus_id=id)
    messages.success(request, f"You successfully deleted the product from your cart")
    product_in_cart.delete_from_cart()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))