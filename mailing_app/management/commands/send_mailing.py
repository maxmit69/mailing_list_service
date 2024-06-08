from django.core.management.base import BaseCommand, CommandError
from mailing_app.models import Mailing
from mailing_app.services import schedule_or_send_mailing, start_scheduler


class Command(BaseCommand):
    help = 'Для отправки рассылки введите команду: python manage.py send_mailing <mailing_id>'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')
        start_scheduler()

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            mailing = Mailing.objects.get(id=mailing_id)
        except Mailing.DoesNotExist:
            raise CommandError(f'Рассылка c id {mailing_id} не существует')

        schedule_or_send_mailing(mailing)
        self.stdout.write(self.style.SUCCESS(f'Рассылка c id {mailing_id} отправлена'))