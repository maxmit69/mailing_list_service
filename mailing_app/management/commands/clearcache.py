from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Очистка кэша сайта при помощи команды: python manage.py clearcache'

    def handle(self, *args, **options):
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Successfully cleared cache'))
