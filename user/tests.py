from django.test import TestCase, Client
from django.contrib.auth.models import User


class TestUser(TestCase):
    fixtures = ['test_data.json']

    @staticmethod
    def logged_client():
        test_client = Client()
        test_client.login(username='guest', password='vfRarYj37Jfp@V3')
        return test_client

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

    def test_registration_fail(self):  # Already existing username
        test_client = Client()
        response = test_client.post('/register', data={'username': 'guest', 'password': 'failTest', 'email': 'failTest@example.com'})
        status_code = response.status_code
        self.assertEqual(status_code, 409)

    def test_login_get(self):
        test_client = Client()
        response = test_client.get('/login')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_login_fail(self):  # Unexisting user
        test_client = Client()
        response = test_client.post('/login', data={'username': 'wrongTest', 'password': 'wrongTest'})
        status_code = response.status_code
        self.assertEqual(status_code, 404)

    def test_login_success(self):
        test_client = Client()
        response = test_client.post('/login', data={'username': 'guest', 'password': 'vfRarYj37Jfp@V3'})
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_login_redirect(self):  # if user is already logged in
        test_client = self.logged_client()

        response = test_client.get('/login')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

        response = test_client.post('/login', data={'username': 'test', 'password': 'test'})
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_registration_redirect(self):  # if user is already logged in
        test_client = self.logged_client()

        response = test_client.get('/register')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

        response = test_client.post('/register', data={'username': 'test', 'password': 'test', 'email': 'test@example.com'})
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_logout(self):
        test_client = self.logged_client()
        response = test_client.get('/logout')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_logout_redirect(self):  # Not logged in
        test_client = Client()
        response = test_client.get('/logout')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_user_page(self):
        test_client = self.logged_client()
        response = test_client.get('/profile')
        status_code = response.status_code
        has_user_name = User.objects.get(username='guest').username in response.content.decode('utf-8')

        self.assertEqual(status_code, 200)
        self.assertTrue(has_user_name)

    def test_user_page_redirect(self):  # Not logged in
        test_client = Client()
        response = test_client.get('/profile')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_user_history(self):
        test_client = self.logged_client()

        response = test_client.get('/history')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_user_history_redirect(self):  # Not logged in
        test_client = Client()
        response = test_client.get('/history')
        status_code = response.status_code
        self.assertEqual(status_code, 302)