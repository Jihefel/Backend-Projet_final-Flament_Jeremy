from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import *
from django.contrib.auth.models import User
from django.template.loader import render_to_string


def index(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            newsletter = form.save()

            # Envoyer un e-mail de confirmation ou effectuer d'autres actions
            send_mail(
                f"{email}, thanks for your subscription to our newsletter",
                "Admin QDP",
                "jfl.jflament@gmail.com",
                [email],
                html_message=render_to_string('mails/subscribe_newsletter.html', {'email': email}),
            )

            return redirect('home')
    else:
        form = NewsletterForm()

    context = {'form': form}  # Ajoutez le formulaire au contexte
    return render(request, 'shop/index.html', context)


def cart(request):
    return render(request, 'shop/cart.html')

def checkout(request):
    return render(request, 'shop/checkout.html')

def contact(request):
    return render(request, 'shop/contact.html')

def login(request):
    return render(request, 'shop/login.html')

def all_products(request):
    return render(request, 'shop/products-left-sidebar-2.html')

def product(request):
    return render(request, 'shop/products-type-1.html')

def signup(request):
    return render(request, 'shop/signup.html')

def article(request):
    return render(request, 'shop/single-blog-1.html')

def blog(request):
    return render(request, 'shop/blog-5.html')


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()

            # Envoyer un e-mail de confirmation ou effectuer d'autres actions
            send_mail(
                "Thanks for subscribing to our newsletter",
                "Admin QDP",
                "jfl.jflament@gmail.com",
                [form.cleaned_data['email']],
                html_message=render_to_string('mails/subscribe_newsletter.html', {'email': form.cleaned_data['email']}),
            )

            return redirect('home')
    else:
        form = NewsletterForm()

    context = {'form': form}
    return render(request, 'shop/components/footer.html', context)

    