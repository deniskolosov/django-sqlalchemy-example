from django.contrib.auth.hashers import make_password, check_password
from django_sorcery.db import databases


db = databases.get('default')


class Country(db.Model):
    pk = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String(256))


class User(db.Model):
    """
    User model which maps to db table User.
    """
    pk = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    name = db.Column(db.String(length=256))
    middle_name = db.Column(db.String(length=256))
    last_name = db.Column(db.String(length=256))
    birth_date = db.Column(db.DateTime())
    password_hash = db.Column(db.String(128))
    nationality = db.ManyToOne(Country, backref=db.backref("users", cascade="all, delete-orphan"))

    def set_password(self, password):
        self.password_hash = make_password(password)

    def check_password(self, password):
        return check_password(self.password_hash, password)

    def get_jwt_token(self):
        pass
