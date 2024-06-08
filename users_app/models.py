from django.contrib.auth.models import AbstractUser
from django.db import models
from mailing_app.models import NULLABLE


# Create your models here.
class User(AbstractUser):
    """ Клиент сервиса """
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=20, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='user_avatars/%Y/%m/%d', verbose_name='аватар', **NULLABLE)
    token = models.CharField(max_length=255, verbose_name='токен', **NULLABLE)
    user_is_blocked = models.BooleanField(default=False, verbose_name='заблокирован')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        permissions = [
            ('can_block_users', 'Может блокировать пользователей сервиса'),
        ]
