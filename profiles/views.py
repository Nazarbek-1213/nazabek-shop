from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from Product.models import Product
from .forms import ProfileForm, AvatarForm

@login_required
def profile_view(request):
    my_products = Product.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "profile.html", {
        "my_products": my_products,
        "cart_count": 0,
    })

@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile_edit.html", {
        "form": form,
        "cart_count": 0,
    })

@login_required
def profile_avatar_upload(request):
    profile = request.user.profile
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    return redirect("profile")

