# Generated by Django 5.0.4 on 2024-06-07 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_is_blocked',
            field=models.BooleanField(default=False, verbose_name='заблокирован'),
        ),
    ]