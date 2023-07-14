from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.paginator import Paginator




def index(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    
    # Infos du site
    infos = InfosQDP.objects.first()

    # Partenaires
    partners = Partenaires.objects.all()
    
    # Promotions
    promos = Promotions.objects.all()

    # Categories
    categories = Categorie.objects.all()
    categories_in_promo = []
    for category in categories:
        if category.promo:
            categories_in_promo.append(category)

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "Email already subscribed.")
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

@login_required(login_url = 'connexion')
def account(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    # Infos du site
    infos = InfosQDP.objects.first()
    
    context = locals()
    return render(request, 'shop/my_account.html', context)

@login_required(login_url = 'connexion')
def edit_account(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()
    
    # Infos du site
    infos = InfosQDP.objects.first()


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


@login_required(login_url='connexion')
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


def cart(request):

    # Infos du site
    infos = InfosQDP.objects.first()

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "Email already subscribed.")
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
    return render(request, 'shop/cart.html', context)

def checkout(request):
    
    # Infos du site
    infos = InfosQDP.objects.first()

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "Email already subscribed.")
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
    return render(request, 'shop/checkout.html', context)

def contact(request):
    
    # Infos du site
    infos = InfosQDP.objects.first()

    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "Email already subscribed.")
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
    return render(request, 'shop/contact.html', context)

def connection(request):
    
    # Infos du site
    infos = InfosQDP.objects.first()

    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

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

@login_required(login_url='connexion')
def deconnection(request):
    logout(request)
    return redirect('home')


@login_required(login_url = 'connexion')
def change_password(request):
    
    # Infos du site
    infos = InfosQDP.objects.first()

    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

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
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    context = locals()  
    return render(request, 'shop/change_password.html', context)

def all_products(request):
    products = Produits.objects.all()
    today = date.today()
    variants_all = Variantes.objects.all()
    categories = Categorie.objects.all()
    
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


     # Pagination des produits
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    # Calculate the start and end indexes for the range of products to display
    per_page = 12  # Number of products per page
    start_index = (int(page_number) - 1) * per_page
    if (int(page_number) * per_page) < products.count():
        end_index = int(page_number) * per_page
    else:
        end_index = products.count()

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

    # Infos du site
    infos = InfosQDP.objects.first()

    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "Email already subscribed.")
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
    

    # Infos du site
    infos = InfosQDP.objects.first()

    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "Email already subscribed.")
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
    
    # Infos du site
    infos = InfosQDP.objects.first()

    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

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
        newsletter_form = NewsletterForm()
        form = BootstrapUserCreationForm()

    context = locals()
    return render(request, 'shop/signup.html', context)


def signup2(request):
    
    # Infos du site
    infos = InfosQDP.objects.first()

    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

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

def article(request):
    
    # Infos du site
    infos = InfosQDP.objects.first()

    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "Email already subscribed.")
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
    
    # Infos du site
    infos = InfosQDP.objects.first()

    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    # Form newsletter
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "Email already subscribed.")
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


    