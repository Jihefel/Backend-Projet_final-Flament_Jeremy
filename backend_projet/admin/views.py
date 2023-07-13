from django.shortcuts import render, redirect
from shop.models import *
from shop.forms import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def admin_home(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    context = locals()
    return render(request, 'admin/home.html', context)

def infos_site(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    infos = InfosQDP.objects.first()
    if request.method == 'POST':
        form = InfosQDPForm(request.POST, instance=infos)
        if form.is_valid():
            form.save()
            messages.success(request, "Infos of the site successfully updated.")
            return redirect('admin_home')
    else:
        form = InfosQDPForm(instance=infos)
    
    context = locals()
    return render(request, 'admin/pages/infos-site/update.html', context)

# MEMBERS
def members_all(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    members = User.objects.all()
    
    context = locals()
    return render(request, 'admin/pages/members/all.html', context)

def members_create(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    members = User.objects.all()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Member successfully created.")
            return redirect('custom_admin:members_all')
    else:
        form = UserCreationForm()
    
    context = locals()
    return render(request, 'admin/pages/members/create.html', context)


def members_delete(request, id):
    member = User.objects.get(id=id)
    messages.success(request, f"Member {member.username} successfully deleted.")
    member.delete()
    
    return redirect('custom_admin:members_all')

def members_update(request, id):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    member = User.objects.get(id=id)
    if request.method == 'POST':
        if member.id == request.user.id:
            form = UserUpdateForm(request.POST, request.FILES, instance=member)
        else:
            form = UserRoleUpdateForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f"Member {member.username} successfully updated.")
            return redirect('custom_admin:members_all')
    else:
        # Initialiser le champ "role" avec la valeur actuelle de l'utilisateur
        initial_data = {'role': member.role}
        if member.id == request.user.id:
            form = UserUpdateForm(instance=member, initial=initial_data)
        else:
            form = UserRoleUpdateForm(instance=member, initial=initial_data)
    
    context = locals()
    return render(request, 'admin/pages/members/update.html', context)

def members_show(request, id):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    member = User.objects.get(id=id)

    context = locals()
    return render(request, 'admin/pages/members/show.html', context)

# Produits
def products_all(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    products = Produits.objects.prefetch_related('productvariant_set__variant').all()
    
    context = locals()
    return render(request, 'admin/pages/products/all.html', context)

def products_create(request):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    products = Produits.objects.all()
    
    if request.method == 'POST':
        form = ProduitsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product successfully created.")
            return redirect('custom_admin:products_all')
    else:
        form = ProduitsForm()
    
    context = locals()
    return render(request, 'admin/pages/products/create.html', context)


def products_delete(request, id):
    product = Produits.objects.get(id=id)
    messages.success(request, f"Product {product.name} successfully deleted.")
    product.delete()
    
    return redirect('custom_admin:products_all')

def products_update(request, id):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    product = Produits.objects.get(id=id)
    variants = product.variations.filter(produits=product)

    
    if request.method == 'POST':
        form = ProduitsForm(request.POST, request.FILES, instance=product)
        variant_forms = []
        qte_forms = []  # Nouvelle liste pour les formulaires de quantité
        for variant in variants:
            prefix = f"variant_{variant.id}"  # Préfixe commun pour les deux types de formulaires
            variant_form = VariantForm(request.POST, instance=variant, prefix=prefix)
            product_variant = ProductVariant.objects.get(product=product, variant=variant)
            qte_form = ProductVariantForm(request.POST, instance=product_variant, prefix=prefix)
            variant_forms.append(variant_form)
            qte_forms.append(qte_form)  # Ajouter le formulaire de quantité à la liste qte_forms

        if form.is_valid() and all([vf.is_valid() for vf in variant_forms]) and all([qf.is_valid() for qf in qte_forms]):
            form.save()
            for variant_form in variant_forms:
                variant_form.save()
            for qte_form in qte_forms:
                qte_form.save()
            messages.success(request, f"Product {product.nom} successfully updated.")
            return redirect('custom_admin:products_all')
    else:
        form = ProduitsForm(instance=product)
        variant_forms = []
        qte_forms = []  # Nouvelle liste pour les formulaires de quantité
        for variant in variants:
            prefix = f"variant_{variant.id}"  # Préfixe commun pour les deux types de formulaires
            variant_form = VariantForm(instance=variant, prefix=prefix)
            product_variant = ProductVariant.objects.get(product=product, variant=variant)
            qte_form = ProductVariantForm(instance=product_variant, prefix=prefix)
            variant_forms.append(variant_form)
            qte_forms.append(qte_form)  # Ajouter le formulaire de quantité à la liste qte_forms
        
    
    context = locals()
    return render(request, 'admin/pages/products/update.html', context)

def products_show(request, id):
    role_id_admin = 1
    role_id_membre = 2
    
    if request.user.id is not None:
        is_admin = Roles.objects.filter(id=role_id_admin, user=request.user).exists()
        is_membre = Roles.objects.filter(id=role_id_membre, user=request.user).exists()

    product = Produits.objects.get(id=id)
    variants = product.variations.all()

    context = locals()
    return render(request, 'admin/pages/products/show.html', context)
