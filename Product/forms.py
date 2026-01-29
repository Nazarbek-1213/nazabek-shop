from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "price", "category", "description", "image", "location_name"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Masalan: iPhone 13"}),
            "price": forms.NumberInput(attrs={"placeholder": "Narx"}),
            "description": forms.Textarea(attrs={"placeholder": "Tavsif..."}),
            "location_name": forms.TextInput(attrs={"placeholder": "Masalan: Toshkent, Chilonzor"}),


        }
