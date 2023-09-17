from django.db import models
from django.contrib.auth.models import User


class UserMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_link = models.CharField(max_length=255)
    main = models.BooleanField()
