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
    # Products
    path('products/', views.products_all, name='products_all'),
    path('products/create', views.products_create, name='products_create'),
    path('products/show/<int:id>', views.products_show, name='products_show'),
    path('products/update/<int:id>', views.products_update, name='products_update'),
    path('products/delete/<int:id>', views.products_delete, name='products_delete'),
    
    
]