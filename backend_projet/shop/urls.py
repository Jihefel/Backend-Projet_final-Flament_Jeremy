from django.urls import path, include
from . import views
from admin import views as admin_views

urlpatterns = [
    path('404/', views.handler404, name='error_404'),
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
    path('my_orders/', views.my_orders, name='my_orders'),
    path('products/', views.all_products, name='all_products'),
    path('products/<int:id>', views.product, name='product'),
    path('signup/', views.signup, name='signup'),
    path('signup2/', views.signup2, name='signup2'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:id>', views.article, name='article'),
    path('admin/', admin_views.admin_home, name='admin_home'),
    path('wishlist/<int:id>', views.wishlist, name='wishlist'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:id>', views.delete_from_cart, name='delete_from_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_code/', views.remove_promo_code, name='remove_code'),
    # Password reset
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]