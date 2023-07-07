from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string

def index(request):
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

def all_products(request):
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
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid() and form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            if user.id == 1:
                user.role = Roles.objects.get(role="admin")
            user.save()

            return redirect('signup2')

        else:
            messages.error(request, "Something went wrong.")

    else:
        newsletter_form = NewsletterForm()
        form = RegistrationForm()

    context = locals()
    return render(request, 'shop/signup.html', context)

# ...

def signup2(request):
    # ...

    if request.method == 'POST':
        form = SignupForm2(request.POST, request.FILES)
        if form.is_valid():
            user_extension = form.save(commit=False)
            user_extension.user = User.objects.last()
            user_extension.save()
            messages.success(request, "Your account has been created. Please now log in.")
            return redirect('home')

    # ...

def article(request):
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


    