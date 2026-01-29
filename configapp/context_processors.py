from django.db.models import Sum
from Product.models import CartItem

def cart_count(request):
    if request.user.is_authenticated:
        total = CartItem.objects.filter(user=request.user).aggregate(s=Sum("quantity"))["s"] or 0
        return {"cart_count": total}
    return {"cart_count": 0}
