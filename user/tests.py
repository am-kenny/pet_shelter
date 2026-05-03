import secrets

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class TestUser(TestCase):
    fixtures = ["test_data.json"]

    @staticmethod
    def logged_client():
        test_client = Client()
        user = get_user_model().objects.get(username="guest")
        test_client.force_login(user)
        return test_client

    def test_registration_get(self):
        test_client = Client()
        response = test_client.get("/register")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_registration_successful(self):
        plain_password = secrets.token_urlsafe(16)
        test_client = Client()
        response = test_client.post(
            "/register",
            data={
                "username": "newuser_reg_ok",
                "email": "newuser_reg_ok@example.com",
                "password1": plain_password,
                "password2": plain_password,
            },
        )
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_registration_fail(self):  # Already existing username
        plain_password = secrets.token_urlsafe(16)
        test_client = Client()
        response = test_client.post(
            "/register",
            data={
                "username": "guest",
                "password1": plain_password,
                "password2": plain_password,
                "email": "failTest@example.com",
            },
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertIn("username", response.context["form"].errors)

    def test_login_get(self):
        test_client = Client()
        response = test_client.get("/login")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_login_fail(self):  # Unexisting user
        test_client = Client()
        response = test_client.post(
            "/login", data={"username": "wrongTest", "password": "wrongTest"}
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_login_success(self):
        user = get_user_model().objects.get(username="guest")
        plain_password = secrets.token_urlsafe(16)
        user.set_password(plain_password)
        user.save()

        test_client = Client()
        response = test_client.post(
            "/login",
            data={"username": "guest", "password": plain_password},
        )
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_login_redirect(self):  # if user is already logged in
        test_client = self.logged_client()

        response = test_client.get("/login")
        status_code = response.status_code
        self.assertEqual(status_code, 302)

        response = test_client.post(
            "/login", data={"username": "test", "password": "test"}
        )
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_registration_redirect(self):  # if user is already logged in
        test_client = self.logged_client()

        response = test_client.get("/register")
        status_code = response.status_code
        self.assertEqual(status_code, 302)

        response = test_client.post(
            "/register",
            data={"username": "test", "password": "test", "email": "test@example.com"},
        )
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_logout(self):
        test_client = self.logged_client()
        response = test_client.get("/logout")
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_logout_redirect(self):  # Not logged in
        test_client = Client()
        response = test_client.get("/logout")
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_user_page(self):
        test_client = self.logged_client()
        response = test_client.get("/profile")
        status_code = response.status_code
        guest = get_user_model().objects.get(username="guest")
        has_user_name = guest.username in response.content.decode("utf-8")

        self.assertEqual(status_code, 200)
        self.assertTrue(has_user_name)

    def test_user_page_redirect(self):  # Not logged in
        test_client = Client()
        response = test_client.get("/profile")
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_user_history(self):
        test_client = self.logged_client()

        response = test_client.get("/history")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_user_history_redirect(self):  # Not logged in
        test_client = Client()
        response = test_client.get("/history")
        status_code = response.status_code
        self.assertEqual(status_code, 302)
