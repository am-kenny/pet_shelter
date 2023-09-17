from django.db import models
from django.contrib.auth.models import User
import animals.models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    media = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(animals.models.Animal, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
