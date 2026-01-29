from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "location", "tg_username"]

    def clean_tg_username(self):
        tg = self.cleaned_data.get("tg_username", "")
        return tg.lstrip("@").replace(" ", "")

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
