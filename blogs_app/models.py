from django.db import models

from mailing_app.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержание')
    image = models.ImageField(upload_to='blogs/', **NULLABLE, verbose_name='изображение')
    count_views = models.IntegerField(default=0, verbose_name='количество просмотров')
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    author = models.ForeignKey(
        'users_app.User',
        on_delete=models.CASCADE, **NULLABLE,
        related_name='blogs',
        verbose_name='автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
