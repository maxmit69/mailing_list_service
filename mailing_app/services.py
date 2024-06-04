import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail

from mailing_app.models import AttemptSend, Mailing

active_schedulers = {}


def send_email(to_email: str, content: str, subject: str) -> str:
    """ Отправка письма
    :param to_email: почта получателя
    :param content: содержание письма
    :param subject: тема письма
    return: статус отправки
    """
    try:
        send_mail(
            subject=subject,
            message=content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False
        )
        return 'OK'
    except Exception as e:
        return f'Письмо не отправлено, ошибка: {str(e)}'


def start_mailing(mailing: Mailing) -> None:
    """ Запуск периодической рассылки
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=mailing.periodicity.total_seconds(), args=[mailing])
    scheduler.start()

    active_schedulers[mailing.id] = scheduler


def send_mailing(mailing: Mailing) -> None:
    """ Отправка рассылки
    :param mailing: рассылка
    return: статус рассылки
    """
    zone = pytz.timezone(settings.TIME_ZONE)  # часовой пояс пользователя
    current_datetime = datetime.datetime.now(zone)  # текущее время в часовом поясе пользователя
    mailings = Mailing.objects.filter(datetime__lte=current_datetime)  # Фильтрация по дате рассылки
    mailings = mailings.exclude(attempt__attempt_status__in=[
        AttemptSend.Status.COMPLETED])  # Фильтрация по статусу

    # Проверяем периодичность
    for mailing in mailings:  # Перебираем рассылки
        last_attempt = AttemptSend.objects.filter(mailing=mailing).order_by('-last_attempt_time').first()  # Последняя попытка
        if last_attempt:  # Если есть попытка
            time_since_last_attempt = current_datetime - last_attempt.last_attempt_time  # Разница между текущим временем и временем попытки
            if time_since_last_attempt.total_seconds() < mailing.periodicity.total_seconds():  # Если разница меньше периодичности
                continue

    # Отправляем письма
    for customer in mailing.customers.all():  # Перебираем клиентов
        attempt = AttemptSend.objects.create(
            mailing=mailing,
            user_attempt=mailing.user_mailing,
            attempt_status=AttemptSend.Status.LAUNCHED
        )  # Создаем попытку
        try:
            # Отправляем письмо
            response = send_email(customer.email, mailing.massage.content, mailing.massage.title)

            attempt.logging = (f'Письмо отправлено: {datetime.datetime.now()}.'
                               f'Клиенту: {customer.email}.'
                               f' Статус отправки: {response}.'
                               )
            attempt.last_attempt_time = attempt.mailing.datetime
            if response == 'OK':
                attempt.attempt_status = AttemptSend.Status.COMPLETED
        except Exception as e:
            attempt.logging = f"{datetime.datetime.now()}: Письмо не отправлено {customer.email}, ошибка: {str(e)}"
            attempt.attempt_status = AttemptSend.Status.CREATED
        finally:
            attempt.save()


def stop_mailing(mailing: Mailing) -> None:
    """ Остановка рассылки
    :param mailing: рассылка
    return: статус рассылки
    """
    AttemptSend.objects.create(
        mailing=mailing,
        user_attempt=mailing.user_mailing,
        attempt_status=AttemptSend.Status.COMPLETED,
        logging=f"{datetime.datetime.now()}: Рассылка остановлена пользователем"
    )

    # Остановка периодической задачи
    if active_schedulers.get(mailing.id):
        active_schedulers[mailing.id].shutdown()
