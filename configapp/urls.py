from tkinter.font import names

from django.urls import path

from configapp.views import *

urlpatterns = [
    path('',dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path("logout/", logout_view, name="logout"),
    path('search/',search_view, name='search'),
    path('chats/', chats_view, name='chats'),
    path('favorite/', favorites_view, name='favorites'),
    path('profile/',profile_view, name='profile'),
    path('cart/',cart_view, name='cart'),
]
