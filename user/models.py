from django.db import models
from django.contrib.auth.models import User


class UserMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ImageField(blank=False, upload_to='user_images/', unique=True)
    main = models.BooleanField()
