from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import  redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        return render(request, "auth\login.html", {"error": "Username yoki password noto‘g‘ri"})

    return render(request, "auth\login.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        return render(request, "auth/login.html", {
            "error": "Username yoki parol noto‘g‘ri"
        })

    return render(request, "auth/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            return render(request, "register.html", {
                "error": "Parollar mos emas"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username mavjud"
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("/")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("login")









def dashboard(request):
    category = request.GET.get("category")

    qs = Product.objects.all().order_by("-created_at")
    if category:
        qs = qs.filter(category=category)

    return render(request, "home.html", {
        "products": qs,
        "cart_count": 0,  # sizda savat count boshqa joydan kelsa, o‘sha logikani qo‘ying
    })






def search_view(request):
    q = (request.GET.get("q") or "").strip()


    qs = Product.objects.all()


    if hasattr(Product, "is_active"):
        qs = qs.filter(is_active=True)

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(category__icontains=q)
        )



    return render(request, "search.html", {
        "products": qs,
        "q": q,

    })


@login_required
def chats_view(request):
    return render(request, "chats.html")

@login_required
def favorites_view(request):
    return render(request, "favorites.html")

@login_required
def profile_view(request):
    return render(request, "profile.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Product.models import Product

@login_required
def cart_view(request):
    cart = request.session.get("cart", {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    items = []
    total = 0
    for p in products:
        qty = cart.get(str(p.id), 0)
        items.append((p, qty))
        total += float(p.price) * qty

    return render(request, "cart.html", {
        "items": items,
        "total": total,
        "cart_count": sum(cart.values()),
    })


