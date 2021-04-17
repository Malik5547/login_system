from django.test import TestCase, Client

from .models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = User(username='admin', password='admin')
        user.save()

    def test_login_success(self):
        self.client.post('/login', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(self.client.session['username'], 'admin')

    def test_login_wrong(self):
        self.client.post('/login', {'username': 'wrong', 'password': 'wrong'})

        self.assertNotIn('username', self.client.session)

    def test_already_logged(self):
        self.client.post('/login', {'username': 'admin', 'password': 'admin'})
        response = self.client.post('/login', {'username': 'user', 'password': 'passwd'})

        self.assertEqual(self.client.session['username'], 'admin')
        self.assertTemplateNotUsed(response, 'login.html')


class SignupTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        first_user = User(username='user1', password='user1')
        first_user.save()

    def test_signup(self):
        self.client.post('/signup', {'username': 'user2', 'password': 'user2'})
        self.assertTemplateUsed('success.html')

    def test_signup_after_login(self):
        response = self.client.post('/login', {'username': 'user1', 'password': 'user1'})
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/signup', {'username': 'user2', 'password': 'user2'})
        self.assertTemplateNotUsed(response, 'signup.html')

        try:
            user = User.objects.get(
                username='user2'
            )
            self.assertNotEqual(user.username, 'user2')
        except (KeyError, User.DoesNotExist):
            pass

    def test_signup_used_username(self):
        users_count = User.objects.all().count()
        self.client.post('/signup', {'username': 'user1', 'password': 'user2'})

        self.assertTemplateNotUsed('/success.html')
        self.assertEqual(users_count, User.objects.all().count())

    def test_signup_empty_fields(self):
        users_count = User.objects.all().count()
        self.client.post('/signup', {'username': '', 'password': ''})

        self.assertTemplateNotUsed('/success.html')
        self.assertEqual(users_count, User.objects.all().count())
