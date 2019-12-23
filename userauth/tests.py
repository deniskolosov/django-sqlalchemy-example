import datetime

from django.test import TestCase, Client
from django.urls import reverse
from sqlalchemy_utils import Country as UtilsCountry

from userauth.models import User, db, Country
from django_sorcery.db import databases


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User(name='Joe')
        self.password = 'foobar'
        self.db = db

    def test_password(self):
        self.user.set_password(self.password)
        db.commit()
        self.assertTrue(self.user.check_password(self.password))


class APITestCase(TestCase):
    def setUp(self):
        self.db = databases.get('default')
        self.user = User.objects.filter(email='joe@mail.com').scalar()
        if self.user is None:
            self.user = User(name='Joe', email='joe@mail.com')
        self.user_country = Country.objects.filter(name='US').scalar()
        if self.user_country is None:
            self.user_country = Country(name=UtilsCountry('US'))
        self.client = Client()
        self.url = reverse('user-auth')
        self.password = 'hello123'
        self.user.name = 'Joe'
        self.user.middle_name = 'Jr'
        self.user.birth_date = datetime.datetime(2018, 5, 19)
        self.user.last_name = 'Doe'
        self.user.set_password(self.password)
        self.token = self.user.get_jwt_token(self.user.email, self.password)
        self.user.nationality = self.user_country

    def test_auth_success(self):
        response = self.client.post(self.url,
                                    data={'email': 'joe@mail.com',
                                          'password': self.password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        results = response.json()
        results.pop('token')
        results.pop('pk')
        self.assertEqual(results, {'first_name': 'Joe',
                                   'last_name': 'Doe',
                                   'middle_name': 'Jr',
                                   'birth_date': '2018-05-19T00:00:00',
                                   'nationality': 'United States'})

    def test_auth_no_user(self):
        response = self.client.post(self.url,
                                    data={'email': 'joe_no_joe@mail.com',
                                          'password': self.password},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        results = response.json()
        self.assertIn('No such user', results['message'])

    def test_incorrect_password(self):
        response = self.client.post(self.url,
                                    data={'email': 'joe@mail.com',
                                          'password': self.password+'456'},
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        results = response.json()
        self.assertIn('Password is incorrect.', results['message'])

    def test_wrong_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        results = response.json()
        self.assertIn('Only POST method is allowed.', results['message'])

    def test_profile_success(self):
        url = reverse('profile')
        response = self.client.get(url, {'password': 'hello123'}, HTTP_Authorization='Bearer {}'.format(self.token))
        self.assertEqual(response.status_code, 200)
        results = response.json()
        results.pop('pk')
        self.assertEqual(results, {
            'first_name': 'Joe',
            'last_name': 'Doe',
            'middle_name': 'Jr',
            'birth_date': '2018-05-19T00:00:00',
            'nationality': 'United States',
            'token': self.token,
        })

    def test_profile_no_token(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        results = response.json()
        self.assertIn('User is not authorized.', results['message'])

    def test_profile_wrong_token(self):
        url = reverse('profile')
        response = self.client.get(url, HTTP_Authorization='Bearer {}'.format(self.token+'foo'))
        self.assertEqual(response.status_code, 401)
        results = response.json()
        self.assertIn('User is not authorized.', results['message'])
