from django.urls import path
from customer.views import *

urlpatterns = [
    path("", chat_list_view, name="chat_list"),
    path("<int:conv_id>/",chat_detail_view, name="chat_detail"),
    path("start/<int:product_id>/", start_chat_view, name="start_chat"),
]
