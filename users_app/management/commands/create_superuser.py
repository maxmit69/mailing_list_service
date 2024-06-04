from django.core.management import BaseCommand

from users_app.models import User


class Command(BaseCommand):
    help = 'Создание суперпользователя'

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='5wUeh@example.com',
            first_name='admin',
            last_name='admin',
        )
        user.set_password('admin')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS('Суперпользователь создан'))
