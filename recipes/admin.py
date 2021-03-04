from django.contrib import admin

from .models import Recipe, Ingredient, IngredientAmount, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "unit",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "author",
        "selected_tags",
    )
    list_filter = (
        "author",
        "tag",
    )
    search_fields = (
        "name",
        "tag__name",
        "author__username",
    )
    empty_value_display = "-пусто-"
    readonly_fields = ("popularity",)

    def selected_tags(self, obj):
        return "; ".join((tag.name for tag in obj.tag.all()))

    def popularity(self, obj):
        return f"{obj.favorited_by.count()} пользователей добавили в избранное"


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "recipe",
        "ingredient",
        "quantity",
    )
    search_fields = (
        "recipe__name",
        "ingredient__name",
    )
    empty_value_display = "-пусто-"


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
