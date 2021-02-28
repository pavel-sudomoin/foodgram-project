from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from django import forms

User = get_user_model()


class CreationForm(UserCreationForm):
    password2 = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email")
        labels = {
            "first_name": _("Имя"),
            "username": _("Имя пользователя"),
            "email": _("Адрес электронной почты"),
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error("password1", error)
        return password1
