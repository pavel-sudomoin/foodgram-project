from django.contrib import admin

from .models import Recipe, Ingredient, IngredientAmount, Tag, Follow, Favorite

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(Follow)
admin.site.register(Favorite)
