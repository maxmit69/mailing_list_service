from django.contrib import admin
from django.utils.safestring import mark_safe
from users_app.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'is_staff', 'is_superuser', 'is_active', 'get_avatar', 'user_is_blocked',
                    'user_is_blocked',)

    def get_avatar(self, obj: User) -> str:
        """ Выводит аватар пользователя в админке
        """
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50" height="50">')

    get_avatar.short_description = 'Аватар'

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='manager').exists() or request.user.is_superuser:
            return True
        return obj.mailing_is_disabled

    def get_fields(self, request, obj=None):
        if request.user.groups.filter(name='manager').exists():
            return ['user_is_blocked']
        return super().get_fields(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='manager').exists():
            return [field.name for field in self.model._meta.fields if field.name != 'user_is_blocked']
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs
