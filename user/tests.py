from django.test import TestCase, Client
from django.contrib.auth.models import User


class TestUser(TestCase):
    def test_registration_get(self):
        test_client = Client()
        response = test_client.get('/register')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_registration_successful(self):
        test_client = Client()
        response = test_client.post('/register', data={'username': 'test', 'password': 'test', 'email': 'test@example.com'})
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_registration_fail(self):
        test_client = Client()
        User.objects.create_user(username='test', password='test')
        response = test_client.post('/register', data={'username': 'test', 'password': 'test', 'email': 'test@example.com'})
        status_code = response.status_code
        self.assertEqual(status_code, 409)

    def test_login_get(self):
        test_client = Client()
        response = test_client.get('/login')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_login_fail(self):
        test_client = Client()
        response = test_client.post('/login', data={'username': 'test', 'password': 'test'})
        status_code = response.status_code
        self.assertEqual(status_code, 404)

    def test_login_success(self):
        test_client = Client()
        User.objects.create_user(username='test', password='test')
        response = test_client.post('/login', data={'username': 'test', 'password': 'test'})
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_login_redirect(self):  # if user is already logged in
        test_client = Client()
        User.objects.create_user(username='test', password='test')
        test_client.login(username='test', password='test')

        response = test_client.get('/login')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

        response = test_client.post('/login', data={'username': 'test', 'password': 'test'})
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_registration_redirect(self):  # if user is already logged in
        test_client = Client()
        User.objects.create_user(username='test', password='test')
        test_client.login(username='test', password='test')

        response = test_client.get('/register')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

        response = test_client.post('/register', data={'username': 'test', 'password': 'test', 'email': 'test@example.com'})
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_logout(self):
        test_client = Client()
        response = test_client.get('/logout')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_logout_redirect(self):
        test_client = Client()
        User.objects.create_user(username='test', password='test')
        test_client.login(username='test', password='test')

        response = test_client.get('/logout')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_user_page(self):
        test_client = Client()
        User.objects.create_user(username='test', password='test')
        test_client.login(username='test', password='test')

        response = test_client.get('/user')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_user_page_redirect(self):
        test_client = Client()
        response = test_client.get('/user')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_user_history(self):
        test_client = Client()
        User.objects.create_user(username='test', password='test')
        test_client.login(username='test', password='test')

        response = test_client.get('/user/history')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_user_history_redirect(self):
        test_client = Client()
        response = test_client.get('/user/history')
        status_code = response.status_code
        self.assertEqual(status_code, 302)