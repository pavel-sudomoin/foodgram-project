from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "followed_by",
        "followed_to",
        "favorite_recipes",
        "added_to_shoplist",
    )
    search_fields = ("user__username",)
    empty_value_display = "-пусто-"
    ordering = ("pk",)

    def followed_by(self, obj):
        return f"{obj.user.followed_by.count()} users"

    def followed_to(self, obj):
        return f"{obj.following.count()} users"

    def favorite_recipes(self, obj):
        return f"{obj.favorites.count()} recipes"

    def added_to_shoplist(self, obj):
        return f"{obj.shoplist.count()} recipes"


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "username", "first_name", "email")
    search_fields = (
        "first_name",
        "username",
        "email",
    )
    empty_value_display = "-пусто-"
    ordering = ("pk",)


admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
