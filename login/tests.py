from django.test import TestCase, Client

from .models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = User(username='admin', password='admin')
        user.save()


    def test_login_success(self):
        client = Client()

        response = self.client.post('/login', {'username': 'admin', 'password': 'admin'})

        print(response._container)
        print(self.client.session.keys())

        self.assertEqual(self.client.session['username'], 'admin')
