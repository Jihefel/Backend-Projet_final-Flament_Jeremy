from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.connection, name='login'),
    path('logout/', views.deconnection, name='logout'),
    path('my-account/', views.account, name='account'),
    path('edit-account/', views.edit_account, name='edit_account'),
    path('subscribe_newsletter/', views.direct_newsletter_subscription, name='direct_newsletter_subscription'),
    path('change_password/', views.change_password, name='change_password'),
    path('products/', views.all_products, name='all_products'),
    path('product/', views.product, name='product'),
    path('signup/', views.signup, name='signup'),
    path('signup2/', views.signup2, name='signup2'),
    path('blogs/', views.article, name='article'),
    path('blog/', views.blog, name='blog'),
]