# Generated by Django 5.0.4 on 2024-05-29 11:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mailing_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='attemptsend',
            name='user_attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='customers',
            name='user_customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='customers',
            field=models.ManyToManyField(related_name='mailing', to='mailing_app.customers', verbose_name='клиенты'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='user_mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='attemptsend',
            name='mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempt', to='mailing_app.mailing', verbose_name='рассылка'),
        ),
        migrations.AddField(
            model_name='message',
            name='user_message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='massage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing_app.message', verbose_name='сообщение'),
        ),
    ]