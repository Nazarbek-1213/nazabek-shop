from django.conf import settings
from django.db import models

class Conversation(models.Model):
    product = models.ForeignKey("Product.Product", on_delete=models.CASCADE, related_name="conversations")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buy_conversations")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sell_conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "buyer", "seller")

    def __str__(self):
        return f"{self.product.title} - {self.buyer} -> {self.seller}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender}: {self.text[:30]}"
