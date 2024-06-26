# Generated by Django 5.0.4 on 2024-06-04 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_app', '0007_alter_mailing_periodicity'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('Создана', 'created'), ('Завершена', 'completed'), ('Запущена', 'launched')], default='Создана', max_length=50, verbose_name='статус рассылки'),
        ),
        migrations.AlterField(
            model_name='attemptsend',
            name='attempt_status',
            field=models.CharField(choices=[('Успешно', 'successful'), ('Неудачно', 'failed')], default='Успешно', max_length=50),
        ),
    ]
