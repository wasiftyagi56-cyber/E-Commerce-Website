from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop', views.all_products, name='shop'),
    path('product/<str:name>', views.single_product, name='single_product'),
    path('signup', views.user_signup, name='user_signup'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
    path('add_product/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart_details, name='cart_details'),
    path('checkout', views.checkout, name='checkout'),
]
