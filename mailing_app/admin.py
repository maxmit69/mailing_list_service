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
    list_display = ('id', 'datetime', 'periodicity', 'massage',)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content',)
    list_filter = ('title',)


@admin.register(models.AttemptSend)
class AttemptSendAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_attempt_time', 'attempt_status', 'logging',)
    list_filter = ('attempt_status', 'last_attempt_time',)
