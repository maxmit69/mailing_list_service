from django.core.management import BaseCommand
from mailing_app.models import Mailing
from mailing_app.services import send_mailing


class Command(BaseCommand):
    help = 'Рассылка всем подписчикам'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки которую нужно запустить')

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            mailing = Mailing.objects.get(id=mailing_id)
            send_mailing(mailing)
            self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing_id} запущена'))
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка {mailing_id} не существует'))
