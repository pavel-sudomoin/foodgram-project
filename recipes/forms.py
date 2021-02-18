from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "image", 'description', 'tag', 'time']
        exclude = ['ingredients']
        #labels = {
        #    "text": _("Текст поста"),
        #    "group": _("Группа"),
        #    "image": _("Изображение"),
        #}
        #help_texts = {
        #    "text": _("Введите текст поста"),
        #    "group": _("Выберите группу, к которой относится пост"),
        #    "image": _("Выберите изображение"),
        #}
        #error_messages = {
        #    "text": {
        #        "required": _("Вы не добавили текст поста"),
        #    },
        #}
