# Generated by Django 5.0.4 on 2024-06-07 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0016_alter_mailing_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='mailing_is_disabled',
            field=models.BooleanField(default=False, verbose_name='рассылка отключена'),
        ),
    ]