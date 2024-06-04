from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Mailing, AttemptSend


@receiver(post_save, sender=Mailing)
def create_attempt_send(sender, instance, created, **kwargs):
    """ Создание попытки рассылки
    :param instance: рассылка
    :param created: создана ли рассылка
    :param kwargs: дополнительные аргументы
    """
    if created:
        AttemptSend.objects.create(
            mailing=instance,
            attempt_status=AttemptSend.Status.CREATED,
            user_attempt=instance.user_mailing,
            last_attempt_time=instance.datetime,
        )
