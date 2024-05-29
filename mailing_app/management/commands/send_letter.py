from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone

from mailing_app.models import Customers, Mailing


class Command(BaseCommand):
    help = 'Рассылка новостей всем подписчикам'

    def handler(self, *args, **kwargs):
        now = timezone.now()
        mailing = Mailing.objects.filter(datetime__lte=now, periodicity__gt=0)
        customers = Customers.objects.all()
        for mail in mailing:
            for customer in customers:
                send_mail(
                    subject=f'Заголовок письма{mail.massage.title}',
                    message=f'Содержание письма{mail.massage.content}',
                    from_email='5wUeh@example.com',
                    recipient_list=[customer.email],
                )
            mail.deleted()
        self.stdout.write(self.style.SUCCESS('Рассылка завершена'))
