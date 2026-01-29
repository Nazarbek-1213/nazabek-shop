from django.urls import path
from . import views

urlpatterns = [


    path("search/", views.search, name="search"),

    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    path("my-products/", views.my_products, name="my_products"),
    path("favorites/", views.favorites_list, name="favorites"),
    path("products/<int:pk>/favorite/", views.favorite_toggle, name="favorite_toggle"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:pk>/", views.cart_remove, name="cart_remove"),
    path("cart/decrease/<int:pk>/", views.cart_decrease, name="cart_decrease"),

    path("products/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("comments/<int:pk>/edit/", views.edit_comment, name="edit_comment"),
    path("comments/<int:pk>/delete/", views.delete_comment, name="delete_comment")
]
