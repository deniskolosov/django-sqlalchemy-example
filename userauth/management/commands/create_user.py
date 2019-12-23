import datetime

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from sqlalchemy_utils import Country as UtilsCountry

from userauth.models import User, db, Country


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            country = Country(name=UtilsCountry('US'))
            user = User(
                name='Joe',
                middle_name='Jr',
                last_name='Doe',
                birth_date=datetime.datetime(2000, 5, 19),
                email='joe@mail.com',
                nationality=country,
            )
            user.set_password('hello123')
            self.stdout.write('Created user')
            db.add(user, country)
            db.commit()
        else:
            self.stdout.write('User was already created!')
