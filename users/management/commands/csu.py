from django.core.management import BaseCommand

from users.models import Users


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = Users.objects.create(email="kakas@gmail.com", username="kakas")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("kakas123")
        user.save()
