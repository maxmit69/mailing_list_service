# Generated by Django 5.0.4 on 2024-05-29 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0004_customers_date_creation_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attemptsend',
            name='attempt_status',
            field=models.CharField(choices=[('created', 'Создана'), ('completed', 'Завершена'), ('launched', 'Запущена')], default='created', max_length=50, verbose_name='статус попытки'),
        ),
    ]