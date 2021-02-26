from django.contrib import admin

from .models import Recipe, Ingredient, IngredientAmount, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "unit",
    )
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "author",
    )
    list_filter = (
        "author",
        "name",
        "tag",
    )
    empty_value_display = "-пусто-"
    readonly_fields = ("popularity",)

    def popularity(self, obj):
        return f"{obj.favorited_by.count()} пользователей добавили в избранное"


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "ingredient", "quantity")
    empty_value_display = "-пусто-"


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
