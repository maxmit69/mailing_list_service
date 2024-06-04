from datetime import datetime

from django.core.management import BaseCommand

from mailing_app.models import Mailing, AttemptSend


class Command(BaseCommand):
    help = 'Остановка рассылки'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки которую нужно остановить')

    def handle(self, *args, **kwargs):
        mailing_id = kwargs['mailing_id']
        try:
            mailing = Mailing.objects.get(id=mailing_id)
            last_attempt = mailing.attempt.last()

            if last_attempt and last_attempt.attempt_status == AttemptSend.Status.LAUNCHED:
                last_attempt.attempt_status = AttemptSend.Status.COMPLETED
                last_attempt.logging = f'{datetime.now()}: Рассылка остановлена пользователем'
                last_attempt.save()
                self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing_id} остановлена'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Идентификатор рассылки {mailing_id} не существует или ещё не запущен'))
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка {mailing_id} не существует'))
