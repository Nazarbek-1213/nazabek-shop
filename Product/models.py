from django.conf import settings
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("elektronika", "Elektronika"),
        ("kiyim", "Kiyim-kechak"),
        ("avto", "Avtomobil"),
        ("uy", "Uy-joy"),
        ("texnika", "Texnika"),
        ("xizmat", "Xizmatlar"),
        ("boshqa", "Boshqalar"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="boshqa")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    location_name = models.CharField(max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    phone_number=models.CharField(max_length=20)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

from django.conf import settings
from django.db import models

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="uniq_user_product_favorite")
        ]

    def __str__(self):
        return f"{self.user} ❤️ {self.product}"

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity * self.product.price

from django.conf import settings
from django.db import models

class Comment(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
