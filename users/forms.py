from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from django import forms

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email")
        labels = {
            "first_name": _("Имя"),
            "username": _("Имя пользователя"),
            "email": _("Адрес электронной почты"),
        }
