import datetime
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
    user_customer = models.ForeignKey('users_app.User', on_delete=models.CASCADE,
                                      verbose_name='пользователь создавши клиента')
    unique_clients = models.BooleanField(default=False, verbose_name='уникальный клиент')

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

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('completed', 'Завершена'),
        ('launched', 'Запущена'),
        ('failed', 'Провалена'),
    ]
    PERIODICITY_CHOICES = [
        ('daily', 'Once a Day'),
        ('weekly', 'Once a Week'),
        ('monthly', 'Once a Month')
    ]
    start_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='дата старта рассылки')
    end_time = models.DateTimeField(**NULLABLE, verbose_name='дата окончания рассылки')
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, default='daily',
                                   verbose_name='периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='launched', verbose_name='статус')
    massage = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    customers = models.ManyToManyField(Customers, related_name='mailing', verbose_name='клиенты')
    user_mailing = models.ForeignKey('users_app.User', on_delete=models.CASCADE, verbose_name='пользователь')
    mailing_is_disabled = models.BooleanField(default=False, verbose_name='рассылка отключена')

    def __str__(self):
        return f"Рассылке стартовала {self.start_time} со статусом {self.status}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('can_disable_mailing', 'Может отключать рассылки'),
        ]


class AttemptSend(models.Model):
    """ Попытка рассылки
    """

    class Status(models.TextChoices):
        SUCCESS = 'success', 'Успешно'
        FAILED = 'failed', 'Неудачно'

    mailing = models.ForeignKey(Mailing, related_name='attempts', on_delete=models.CASCADE, verbose_name='рассылка')
    last_attempt_time = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    attempt_status = models.CharField(max_length=50, choices=Status.choices, default=Status.SUCCESS)
    logging = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')
    user_attempt = models.ForeignKey('users_app.User', on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f"Попытка рассылки в {self.last_attempt_time} со статусом {self.attempt_status}"

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
