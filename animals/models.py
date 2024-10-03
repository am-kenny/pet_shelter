from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Sex(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Animal(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=255)
    availability = models.BooleanField()
    description = models.TextField()
    healthy = models.BooleanField()

    def __str__(self):
        return f"{self.name} ({self.type})"


class AnimalMedia(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    media = models.ImageField(blank=False, upload_to='animal_images/', unique=True)
    is_main = models.BooleanField()


class Schedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-start_time"]

    @property
    def is_past_due(self):
        return datetime.now() > self.start_time
