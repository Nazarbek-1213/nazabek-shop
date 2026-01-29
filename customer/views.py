from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404, redirect, render

from Product.models import Product
from .models import Conversation, Message


@login_required
def start_chat_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    seller = product.owner
    buyer = request.user

    # o'zingizga yozish bo'lmasin
    if buyer == seller:
        return redirect("product_detail", product_id)

    conv, _ = Conversation.objects.get_or_create(
        product=product,
        buyer=buyer,
        seller=seller,
    )
    return redirect("chat_detail", conv.id)


@login_required
def chat_list_view(request):
    user = request.user
    qs = Conversation.objects.filter(Q(buyer=user) | Q(seller=user)).annotate(
        last_time=Max("messages__created_at")
    ).order_by("-last_time", "-created_at")

    return render(request, "chat_list.html", {
        "conversations": qs,
        "cart_count": 0,
    })


@login_required
def chat_detail_view(request, conv_id):
    conv = get_object_or_404(Conversation, id=conv_id)

    # faqat buyer yoki seller ko'ra oladi
    if request.user not in (conv.buyer, conv.seller):
        return redirect("chats")

    if request.method == "POST":
        text = (request.POST.get("text") or "").strip()
        if text:
            Message.objects.create(conversation=conv, sender=request.user, text=text)
        return redirect("chat_detail", conv.id)

    msgs = conv.messages.select_related("sender").all()

    return render(request, "chat_detail.html", {
        "conv": conv,
        "messages": msgs,
        "cart_count": 0,
    })
