from django.shortcuts import render, redirect
from shop.models import *
from shop.forms import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def admin_home(request):
    return render(request, 'admin/home.html')

def infos_site(request):
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
    members = User.objects.all()
    
    context = locals()
    return render(request, 'admin/pages/members/all.html', context)

def members_create(request):
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
    member = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f"Member {member.username} successfully updated.")
            return redirect('custom_admin:members_all')
    else:
        # Initialiser le champ "role" avec la valeur actuelle de l'utilisateur
        initial_data = {'role': member.role}
        form = UserUpdateForm(instance=member, initial=initial_data)
    
    context = locals()
    return render(request, 'admin/pages/members/update.html', context)

def members_show(request, id):
    member = User.objects.get(id=id)

    context = locals()
    return render(request, 'admin/pages/members/show.html', context)


# AVATARS

def avatars_all(request):
    avatars = Avatar.objects.all()
    
    context = locals()
    return render(request, 'admin/pages/avatars/all.html', context)

def avatars_create(request):
    avatars = Avatar.objects.all()
    
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Avatar successfully created.")
            return redirect('custom_admin:avatars_all')
    else:
        form = AvatarForm()
    
    context = locals()
    return render(request, 'admin/pages/avatars/create.html', context)