from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Pays, President
from .forms import PaysForm, PresidentForm


def index(request):
    if request.method == 'POST':
        pays_form = PaysForm(request.POST)
        president_form = PresidentForm(request.POST, request.FILES)

        if pays_form.is_valid():
            pays_form.save()
            return redirect('index')

        if president_form.is_valid():
            president_form.save()
            return redirect('index')
    else:
        pays_form = PaysForm()
        president_form = PresidentForm()

    pays = Pays.objects.all()
    presidents = President.objects.all()
    context = locals()
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
