# Generated by Django 5.0.4 on 2024-05-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0003_message_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customers',
            name='date_creation_client',
            field=models.DateTimeField(auto_now_add=True, default='2024-05-29 16:45:00', verbose_name='дата создания'),
            preserve_default=False,
        ),
    ]