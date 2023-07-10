from django.urls import path
from . import views

app_name = 'custom_admin'
urlpatterns = [
    path('admin/', views.admin_home, name='admin_home'),
    # Infos
    path('infos-site/update/', views.infos_site, name='infos_site'),
    # Members
    path('members/', views.members_all, name='members_all'),
    path('members/create', views.members_create, name='members_create'),
    path('members/show/<int:id>', views.members_show, name='members_show'),
    path('members/update/<int:id>', views.members_update, name='members_update'),
    path('members/delete/<int:id>', views.members_delete, name='members_delete'),
]