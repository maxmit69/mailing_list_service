# Generated by Django 5.0.4 on 2024-06-04 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0010_rename_datetime_mailing_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attemptsend',
            name='attempt_status',
            field=models.CharField(choices=[('success', 'Успешно'), ('failed', 'Неудачно')], default='success', max_length=50),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('created', 'Создана'), ('completed', 'Завершена'), ('launched', 'Запущена'), ('failed', 'Провалена')], default='created', max_length=10, verbose_name='статус'),
        ),
    ]
