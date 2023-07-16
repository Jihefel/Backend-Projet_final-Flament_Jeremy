from django.urls import path
from . import views

app_name = 'custom_admin'
urlpatterns = [
    
    path('admin/', views.admin_home, name='admin_home'),
    # Infos
    path('infos-site/update/', views.infos_site, name='infos_site'),
    # Mailbox
    path('contacts/', views.contacts_all, name='contacts_all'),
    path('contacts/reply/<int:id>', views.contacts_reply, name='reply_msg'),
    # Partners
    path('partners/', views.partners_all, name='partners_all'),
    path('partners/create', views.partners_create, name='partners_create'),
    path('partners/update/<int:id>', views.partners_update, name='partners_update'),
    path('partners/delete/<int:id>', views.partners_delete, name='partners_delete'),
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
    # Promotions
    path('promos/', views.promos_all, name='promos_all'),
    path('promos/create', views.promos_create, name='promos_create'),
    path('promos/extra/', views.extra_promo, name='extra_promo'),
    path('promos/show/<int:id>', views.promos_show, name='promos_show'),
    path('promos/update/<int:id>', views.promos_update, name='promos_update'),
    path('promos/delete/<int:id>', views.promos_delete, name='promos_delete'),
    # Categories
    path('categories/', views.categories_all, name='categories_all'),
    path('categories/create', views.categories_create, name='categories_create'),
    path('categories/show/<int:id>', views.categories_show, name='categories_show'),
    path('categories/update/<int:id>', views.categories_update, name='categories_update'),
    path('categories/delete/<int:id>', views.categories_delete, name='categories_delete'),
    
    
]