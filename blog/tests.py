from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

import animals.models
import blog.models


class TestFeedback(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        self.test_animal = animals.models.Animal.objects.get(id=1)

    @staticmethod
    def logged_client():
        test_client = Client()
        user = get_user_model().objects.get(username="guest")
        test_client.force_login(user)
        return test_client

    def test_feedback_get(self):
        test_client = Client()
        response = test_client.get("/blog/feedbacks")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_feedback_get_2(self):
        test_client = Client()
        response = test_client.get(
            "/blog/feedbacks", data={"animal_id": self.test_animal.id}
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_feedback_post(self):
        test_client = self.logged_client()
        response = test_client.post(
            reverse("feedbacks"),
            data={
                "title": "test",
                "text": "test",
                "media": "test",
                "animal": self.test_animal.id,
            },
        )
        status_code = response.status_code
        feedback = blog.models.Feedback.objects.get(
            title="test", text="test", media="test"
        )
        self.assertEqual(feedback.title, "test")
        self.assertEqual(feedback.text, "test")
        self.assertEqual(feedback.media, "test")
        self.assertEqual(feedback.animal.id, self.test_animal.id)
        self.assertEqual(status_code, 302)

    def test_feedback_post_fail(self):  # Not logged in
        test_client = Client()
        response = test_client.post(
            reverse("feedbacks"),
            data={
                "title": "test",
                "text": "test",
                "media": "test",
                "animal": self.test_animal.id,
            },
        )
        status_code = response.status_code
        is_feedback = blog.models.Feedback.objects.filter(
            title="test", text="test", media="test"
        ).exists()
        self.assertFalse(is_feedback)
        self.assertEqual(status_code, 200)

    def test_feedback_post_fail_2(self):  # Unexisting animal
        test_client = self.logged_client()
        response = test_client.post(
            reverse("feedbacks"),
            data={
                "title": "test",
                "text": "test",
                "media": "test",
                "animal": 777,
            },
        )
        status_code = response.status_code
        is_feedback = blog.models.Feedback.objects.filter(
            title="test", text="test", media="test"
        ).exists()
        self.assertFalse(is_feedback)
        self.assertEqual(status_code, 200)

    def test_feedback_post_requires_completed_walk_with_animal(self):
        """Guest has past walks for animal 1 but not for animal 2."""
        test_client = self.logged_client()
        animal_no_walk = animals.models.Animal.objects.get(id=2)
        response = test_client.post(
            reverse("feedbacks"),
            data={
                "title": "no walk",
                "text": "no walk",
                "media": "n/a",
                "animal": animal_no_walk.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(blog.models.Feedback.objects.filter(title="no walk").exists())


class TestBlog(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        self.test_blog = blog.models.Blog.objects.first()

    def test_blog_page(self):
        test_client = Client()
        response = test_client.get("/blog/")
        status_code = response.status_code
        has_blog_title = self.test_blog.title in response.content.decode("utf-8")
        self.assertEqual(status_code, 200)
        self.assertTrue(has_blog_title)

    def test_blog_post(self):
        test_client = Client()
        response = test_client.get(reverse("blog_post", args=[self.test_blog.id]))
        status_code = response.status_code
        has_blog_title = self.test_blog.title in response.content.decode("utf-8")
        self.assertEqual(status_code, 200)
        self.assertTrue(has_blog_title)

    def test_blog_post_fail(self):  # Unexisting blog post
        test_client = Client()
        response = test_client.get(reverse("blog_post", args=[777]))
        status_code = response.status_code
        self.assertEqual(status_code, 404)
