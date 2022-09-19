from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):

    def handle(self, *args, **options):
        username = input('Username: ')
        email = input('Email of user: ')
        is_superuser=input('Is supper user: ') == '1'
        password=input('Password: ')
        confirmPassword=input('Confirm Password: ')

        if password == confirmPassword:
            User.objects.create(
                username=username,
                email=email,
                is_superuser=is_superuser,
                password=make_password(password)
            )

            self.stdout.write(self.style.SUCCESS('Created user'))
        else:
            self.stdout.write(self.style.ERROR('Cannot create user'))

