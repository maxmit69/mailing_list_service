import logging
import smtplib
from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore
from mailing_app.models import Mailing, AttemptSend
from django.utils import timezone
from dateutil.relativedelta import relativedelta

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


def start_scheduler():
    # Запускаем задачи по расписанию
    if not scheduler.running:
        scheduler.start()


def calculate_next_send_time(mailing):
    """Вычисляет время следующей попытки отправки рассылки"""
    last_attempt = AttemptSend.objects.filter(mailing=mailing).order_by('-last_attempt_time').first()
    current_time = timezone.now()

    if not last_attempt:
        # Если попыток отправки еще не было, используем start_time
        next_send_time = mailing.start_time
    else:
        # Иначе используем время последней попытки
        last_attempt_time = last_attempt.last_attempt_time

        # Проверяем, находится ли текущее время в пределах временного интервала рассылки
        if mailing.start_time <= current_time <= mailing.end_time:
            # Если периодичность - ежедневно и прошло более 1 дня с последней попытки
            if mailing.periodicity == 'daily' and (current_time - last_attempt_time).days >= 1:
                next_send_time = last_attempt_time + relativedelta(days=1, hours=mailing.start_time.hour,
                                                                   minutes=mailing.start_time.minute)
            # Если периодичность - еженедельно и прошло более 7 дней с последней попытки
            elif mailing.periodicity == 'weekly' and (current_time - last_attempt_time).days >= 7:
                next_send_time = last_attempt_time + relativedelta(weeks=1, hours=mailing.start_time.hour,
                                                                   minutes=mailing.start_time.minute)
            # Если периодичность - ежемесячно и прошло более 30 дней с последней попытки
            elif mailing.periodicity == 'monthly' and (current_time - last_attempt_time).days >= 30:
                next_send_time = last_attempt_time + relativedelta(days=30, hours=mailing.start_time.hour,
                                                                   minutes=mailing.start_time.minute)
            else:
                next_send_time = None  # Или можно установить на будущее время по умолчанию
        else:
            next_send_time = None  # Время вне интервала рассылки

    return next_send_time


def schedule_or_send_mailing(mailing):
    """Планирование или отправка рассылки
    """
    next_send_time = calculate_next_send_time(mailing)

    if next_send_time:
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime = datetime.now(zone)
        if next_send_time <= current_datetime:
            # Запуск немедленно
            send_mailing(mailing.pk)
        else:
            # Планировать задачу
            schedule_task(next_send_time, mailing.pk)
    else:
        pass


def send_mailing(mailing_id):
    """Отправка рассылки
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        logger.error(f"Рассылка с id {mailing_id} не существует")
        return

    for customer in mailing.customers.all():
        # Отправляем письмо
        try:
            send_mail(
                subject=mailing.massage.title,
                message=mailing.massage.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[customer.email],
                fail_silently=False
            )
            response = f'Почта отправлена успешно пользователю {customer.full_name} на адрес {customer.email}'
            attempt_status = AttemptSend.Status.SUCCESS
        except smtplib.SMTPException as e:
            response = f'Не удалось отправить письмо пользователю {customer.full_name}. Ошибка: {str(e)}'
            attempt_status = AttemptSend.Status.FAILED
        except ConnectionError as ce:
            response = (f'Не удалось отправить письмо пользователю {customer.full_name}.'
                        f' ConnectionError: {str(ce)}')
            attempt_status = AttemptSend.Status.FAILED
        except TimeoutError as te:
            response = (f'Не удалось отправить письмо пользователю {customer.full_name}.'
                        f' TimeoutError: {str(te)}')
            attempt_status = AttemptSend.Status.FAILED
        except Exception as ex:
            response = (f'Не удалось отправить письмо пользователю {customer.full_name}.'
                        f' Непредвиденная ошибка: {str(ex)}')
            attempt_status = AttemptSend.Status.FAILED

        # Запись попытки в базу данных
        AttemptSend.objects.create(
            mailing=mailing,
            logging=response,
            attempt_status=attempt_status,
            user_attempt=mailing.user_mailing,
        )

        # Обновляем статус рассылки
        if attempt_status == AttemptSend.Status.SUCCESS and mailing.end_time != datetime.now():
            mailing.status = Mailing.STATUS_CHOICES[2][0]  # Запущена
        elif attempt_status == AttemptSend.Status.FAILED:
            mailing.status = Mailing.STATUS_CHOICES[3][0]  # Провалена
        elif mailing.end_time and mailing.end_time <= datetime.now():
            mailing.status = Mailing.STATUS_CHOICES[1][0]  # Завершена
        mailing.save()


def schedule_task(start_time, mailing_id):
    # Запускаем задачу в заданное время
    scheduler.add_job(send_mailing, 'date', run_date=start_time, args=[mailing_id])
