from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


def index(request):
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
    return render(request, 'shop/index.html', context)

@login_required(login_url = 'connexion')
def account(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()
    
    context = locals()
    return render(request, 'shop/my_account.html', context)

@login_required(login_url = 'connexion')
def edit_account(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

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
                messages.success(request, f"Bienvenue {user.username}")
                return redirect('home')
            else:
                if not username in User.objects.all():
                    messages.error(request, "Compte inconnu.")
                else :
                    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
                
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

def product(request):
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
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    if request.method == 'POST':
        form = BootstrapUserCreationForm(request.POST)

        if form.is_valid() and form.is_valid():
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
                first_user.role.set([Roles.objects.get(role='admin')])
                first_user.is_superuser = True
                first_user.is_staff = True
                first_user.save()
            else:
                new_user.role.set([Roles.objects.get(role='membre')])
                new_user.save()

            return redirect('signup2')

        else:
            messages.error(request, "Something went wrong.")

    else:
        newsletter_form = NewsletterForm()
        form = BootstrapUserCreationForm()

    context = locals()
    return render(request, 'shop/signup.html', context)

# ...

def signup2(request):
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
            return redirect('login')
    else:
        form = SignupForm2()
        newsletter_form = NewsletterForm()

    context = locals()
    return render(request, 'shop/signup2.html', context)

def article(request):
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


    