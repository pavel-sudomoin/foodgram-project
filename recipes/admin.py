from django.contrib import admin

from .models import Unit, Recipe, Ingredient, IngredientAmount, Tag

admin.site.register(Tag)
admin.site.register(Unit)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
