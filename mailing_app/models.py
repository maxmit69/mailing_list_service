from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Customers(models.Model):
    """ Клиент сервиса
    """
    full_name = models.CharField(max_length=100, verbose_name="Ф.И.О.")
    email = models.EmailField(verbose_name='почта')
    comment = models.TextField(verbose_name='комментарии', **NULLABLE)
    date_creation_client = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    user_customer = models.ForeignKey('users_app.User', on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    """ Сообщение для рассылки
    """
    title = models.CharField(max_length=150, verbose_name='тема письма')
    content = models.TextField(verbose_name='содержание письма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания письма')
    user_message = models.ForeignKey('users_app.User', on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    """ Рассылка (настройка)
    """

    class Status(models.TextChoices):
        CREATED = 'Создана', 'created'
        COMPLETED = 'Завершена', 'completed'
        LAUNCHED = 'Запущена', 'launched'

    datetime = models.DateTimeField(auto_now_add=True, verbose_name='дата первой отправки')
    periodicity = models.DurationField(verbose_name='периодичность', help_text='в секундах', **NULLABLE)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.CREATED,
                              verbose_name='статус рассылки')
    massage = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    customers = models.ManyToManyField(Customers, related_name='mailing', verbose_name='клиенты')
    user_mailing = models.ForeignKey('users_app.User', on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.massage}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class AttemptSend(models.Model):
    """ Попытка рассылки
    """

    class Status(models.TextChoices):
        SUCCESS = 'Успешно', 'successful'
        FAILED = 'Неудачно', 'failed'

    mailing = models.ForeignKey(Mailing, related_name='attempt', on_delete=models.CASCADE, verbose_name='рассылка')
    last_attempt_time = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    attempt_status = models.CharField(max_length=50, choices=Status.choices, default=Status.SUCCESS)
    logging = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')
    user_attempt = models.ForeignKey('users_app.User', on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.mailing} {self.attempt_status}'

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
        get_latest_by = 'last_attempt_time'
