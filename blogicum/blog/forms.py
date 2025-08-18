from django import forms
from django.contrib.auth.models import Group


class GroupForm(forms.ModelForm):
    """Форма для Group: заменяем двойной select на обычный мультиселект."""

    class Meta:
        model = Group
        fields = "__all__"
        widgets = {
            "permissions": forms.SelectMultiple(),
        }
