from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name', 'email')
    list_filter = ('username', 'email',)


admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
