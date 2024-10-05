from django.db import models
import animals.models
from pet_shelter import settings


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    media = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    animal = models.ForeignKey(animals.models.Animal, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
