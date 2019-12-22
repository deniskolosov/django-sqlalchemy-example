from datetime import timedelta, date
from sqlalchemy_utils import EmailType, CountryType

from django.contrib.auth.hashers import make_password, check_password
from django_sorcery.db import databases
from jose import jws

db = databases.get('default')
db.url = 'postgresql://postgres:***@localhost:5432/postgres'


class Country(db.Model):
    pk = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(CountryType)


class User(db.Model):
    """
    User model which maps to db table User.
    """
    pk = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String(length=256))
    middle_name = db.Column(db.String(length=256))
    last_name = db.Column(db.String(length=256))
    birth_date = db.Column(db.DateTime())
    email = db.Column(EmailType, unique=True)
    password_hash = db.Column(db.String(128))
    nationality = db.ManyToOne(Country, backref=db.backref("users", cascade="all, delete-orphan"))
    token = db.Column(db.String(512))

    def set_password(self, password):
        """
        Save password hash to db using standard django function.
        """
        self.password_hash = make_password(password)
        db.commit()

    def check_password(self, password):
        """
        Compare given password with saved hash using django function.
        """
        return check_password(password, self.password_hash)

    def get_jwt_token(self, user_email, password):
        """
        Get jwt token from user email and password, which will expire in 7 days.
        """
        expiry = date.today() + timedelta(days=7)
        self.token = jws.sign({'email': user_email, 'expiry': expiry.strftime('%Y-%m-%d')}, password, algorithm='HS256')
        # We use django-sorcery middleware to commit in the end of each request.
        db.flush()
        return self.token
