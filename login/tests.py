from django.test import TestCase, Client

from .models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = User(username='admin', password='admin')
        user.save()

    def test_login_success(self):
        response = self.client.post('/login', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(self.client.session['username'], 'admin')

    def test_login_wrong(self):
        response = self.client.post('/login', {'username': 'wrong', 'password': 'wrong'})

        self.assertNotIn('username', self.client.session)

    def test_already_logged(self):
        self.client.post('/login', {'username': 'admin', 'password': 'admin'})
        response = self.client.post('/login', {'username': 'user', 'password': 'passwd'})

        self.assertEqual(self.client.session['username'], 'admin')
        self.assertTemplateNotUsed(response, 'login.html')
