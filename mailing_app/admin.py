from django.contrib import admin
from mailing_app import models


# Register your models here.
@admin.register(models.Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'comment',)
    list_filter = ('email', 'full_name',)
    search_fields = ('full_name',)
    empty_value_display = '-empty-'


@admin.register(models.Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'periodicity', 'massage', 'user_mailing',)
    list_filter = ('start_time', 'periodicity', 'user_mailing',)

    # Если пользователь - manager, то  может редактируем только поле mailing_is_disabled
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='manager').exists() or request.user.is_superuser:
            return True
        return obj.mailing_is_disabled

    def get_fields(self, request, obj=None):
        if request.user.groups.filter(name='manager').exists():
            return ['mailing_is_disabled']
        return super().get_fields(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='manager').exists():
            return [field.name for field in self.model._meta.fields if field.name != 'mailing_is_disabled']
        return super().get_readonly_fields(request, obj)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content',)
    list_filter = ('title',)


@admin.register(models.AttemptSend)
class AttemptSendAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_attempt_time', 'attempt_status', 'logging',)
    list_filter = ('attempt_status', 'last_attempt_time',)
