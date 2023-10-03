from django.contrib.auth.models import User
from django.test import TestCase, Client

import animals.models
import blog.models


class TestFeedback(TestCase):
    def setUp(self):
        new_sex = animals.models.Sex.objects.create(name='test')

        self.test_animal = animals.models.Animal.objects.create(name='test', type='test', sex=new_sex, age=2,
                                                                breed='test',
                                                                availability=1, description='test', healthy=1)
        self.test_user = User.objects.create_user(username='test', password='test')

    def test_feedback_get(self):
        test_client = Client()
        test_client.login(username='test', password='test')
        response = test_client.get('/blog/feedbacks')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_feedback_get_2(self):
        test_client = Client()
        test_client.login(username='test', password='test')
        response = test_client.get('/blog/feedbacks', data={'animal_id': self.test_animal.id})
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_feedback_post(self):
        test_client = Client()
        test_client.login(username='test', password='test')
        response = test_client.post('/blog/feedbacks', data={
            'title': 'test',
            'text': 'test',
            'media': 'test',
            'animal': self.test_animal.id,
        })
        status_code = response.status_code
        feedback = blog.models.Feedback.objects.get()
        self.assertEqual(feedback.title, 'test')
        self.assertEqual(feedback.text, 'test')
        self.assertEqual(feedback.media, 'test')
        self.assertEqual(feedback.animal.id, self.test_animal.id)
        self.assertEqual(status_code, 200)

    def test_animal_feedback_post(self):
        test_client = Client()
        test_client.login(username='test', password='test')
        response = test_client.post(f'/animals/{self.test_animal.id}', data={
            'title': 'test',
            'text': 'test',
            'media': 'test',
        })
        status_code = response.status_code
        feedback = blog.models.Feedback.objects.get()
        self.assertEqual(feedback.title, 'test')
        self.assertEqual(feedback.text, 'test')
        self.assertEqual(feedback.media, 'test')
        self.assertEqual(feedback.animal.id, self.test_animal.id)
        self.assertEqual(status_code, 200)


class TestBlog(TestCase):
    def setUp(self):
        self.test_blog = blog.models.Blog.objects.create(title="test",
                                                           text="test")

    def test_blog_page(self):
        test_client = Client()
        response = test_client.get('/blog/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_blog_post(self):
        test_client = Client()
        response = test_client.get(f'/blog/{self.test_blog.id}')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_blog_post_fail(self):
        test_client = Client()
        response = test_client.get(f'/blog/15')
        status_code = response.status_code
        self.assertEqual(status_code, 404)