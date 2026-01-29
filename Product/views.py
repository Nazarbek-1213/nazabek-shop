from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from profiles.views import  *

from .forms import ProductForm
from .models import Product, CartItem

from .models import Favorite

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = product.comments.select_related("user")

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(
            user=request.user,
            product=product
        ).exists()

    return render(request, "product_detail.html", {
        "product": product,
        "is_favorited": is_favorited,
        "comments": comments,

    })


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.owner = request.user
            p.save()
            return redirect("product_detail", pk=p.id)
    else:
        form = ProductForm()

    return render(request, "product_create.html", {
        "form": form,
        "cart_count": 0,
    })


@login_required
def product_edit(request, pk):
    # faqat owner edit qila oladi
    product = get_object_or_404(Product, pk=pk, owner=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_detail", pk=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, "product_edit.html", {
        "form": form,
        "product": product,
        "cart_count": 0,
    })


@login_required
def product_delete(request, pk):
    # faqat owner delete qila oladi
    product = get_object_or_404(Product, pk=pk, owner=request.user)

    if request.method == "POST":
        product.delete()
        return redirect("profile")

    return render(request, "product_delete.html", {
        "product": product,
        "cart_count": 0,
    })


@login_required
def my_products(request):
    qs = Product.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "my_products.html", {
        "products": qs,
        "cart_count": 0,
    })


def search(request):
    q = (request.GET.get("q") or "").strip()
    category = (request.GET.get("category") or "").strip()

    qs = Product.objects.filter(is_active=True)

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location_name__icontains=q)
        )
    if category:
        qs = qs.filter(category=category)

    return render(request, "search.html", {
        "products": qs,
        "q": q,
        "category": category,
        "cart_count": 0,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from .models import Product, Favorite

@login_required
def favorites_list(request):
    qs = (Favorite.objects
          .filter(user=request.user)
          .select_related("product", "product__owner")
          .order_by("-created_at"))
    return render(request, "favorites.html", {
        "favorites": qs,
        "cart_count": 0,
    })

@login_required
def favorite_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # ixtiyoriy: o‘z e’lonini saqlamasin
    if product.owner_id == request.user.id:
        return redirect("profile")

    fav = Favorite.objects.filter(user=request.user, product=product).first()
    if fav:
        fav.delete()
    else:
        Favorite.objects.create(user=request.user, product=product)

    # qaysi sahifadan bosilgan bo‘lsa, o‘sha yerga qaytaradi
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))



from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product,CartItem

# 🛒 Savat sahifasi
@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")

    total = sum(i.total_price for i in items)

    return render(request, "cart.html", {
        "items": items,
        "total": total,
    })



@login_required
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # o‘z e’lonini savatga qo‘shmasin
    if product.owner == request.user:
        return redirect("profile")

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))


# ➖ Savatdan olib tashlash
@login_required
def cart_remove(request, pk):
    item = get_object_or_404(
        CartItem,
        pk=pk,
        user=request.user
    )
    item.delete()
    return redirect("cart")


# 🔽 Miqdorni kamaytirish
@login_required
def cart_decrease(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect("cart")


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Comment

@login_required
def add_comment(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # ❌ o'z e'loniga yozolmasin
    if product.owner_id == request.user.id:
        messages.warning(request, "O‘z e’loningizga sharh yozib bo‘lmaydi.")
        return redirect("product_detail", pk=product.id)

    if request.method == "POST":
        text = (request.POST.get("text") or "").strip()
        if not text:
            messages.error(request, "Sharh bo‘sh bo‘lishi mumkin emas.")
            return redirect("product_detail", pk=product.id)

        Comment.objects.create(product=product, user=request.user, text=text)
        messages.success(request, "Sharh qo‘shildi.")
    return redirect("product_detail", pk=product.id)


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # ✅ faqat o'zi yozganini edit qilsin
    if comment.user_id != request.user.id:
        messages.error(request, "Bu sharh sizniki emas.")
        return redirect("product_detail", pk=comment.product_id)

    if request.method == "POST":
        text = (request.POST.get("text") or "").strip()
        if not text:
            messages.error(request, "Sharh bo‘sh bo‘lishi mumkin emas.")
            return render(request, "comment_edit.html", {"comment": comment})

        comment.text = text
        comment.save()
        messages.success(request, "Sharh yangilandi.")
        return redirect("product_detail", pk=comment.product_id)

    return render(request, "comment_edit.html", {"comment": comment})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # ✅ faqat o'zi o'chirsin
    if comment.user_id != request.user.id:
        messages.error(request, "Bu sharh sizniki emas.")
        return redirect("product_detail", pk=comment.product_id)

    if request.method == "POST":
        pid = comment.product_id
        comment.delete()
        messages.success(request, "Sharh o‘chirildi.")
        return redirect("product_detail", pk=pid)

    return render(request, "comment_delete.html", {"comment": comment})

from django.db.models import Sum
from Product.models import CartItem  # CartItem qaysi appda bo‘lsa, o‘shadan import qiling



