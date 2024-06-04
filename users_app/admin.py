from django.contrib import admin
from django.utils.safestring import mark_safe
from users_app.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'avatar', 'get_avatar')

    def get_avatar(self, obj: User) -> str:
        """ Выводит аватар пользователя в админке
        """
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50" height="50">')

    get_avatar.short_description = 'Аватар'
