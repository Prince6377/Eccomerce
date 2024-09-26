from django.urls import path
from accounts.views import *

urlpatterns = [
    path("login/" , login_page , name='login'),
    path("register/" , register_page , name='register'),
    path("activate/<str:email_token>/" , email_verified , name = 'email_verify'),
    path('add-to-cart/<str:uid>/', add_to_cart, name='add_to_cart'),
    path('cart/' , cart , name= 'cart'),
    path('remove-cart/<int:Cart_item_id>/', remove_cart, name='remove_cart'),


]
