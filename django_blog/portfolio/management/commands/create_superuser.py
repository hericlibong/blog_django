import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "mot_de_passe")


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='hericlibong@gmail.com',
                password=password
            )
            self.stdout.write('Superuser created successfully')
