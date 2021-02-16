from django.contrib import admin

from .models import Recipe, Ingredient, IngredientAmount, Tag

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
