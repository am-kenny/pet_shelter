from django.db import models
from django.contrib.auth.models import AbstractUser

from pet_shelter import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'auth_user'

class UserMedia(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    media = models.ImageField(blank=False, upload_to='user_images/', unique=True)
    main = models.BooleanField()
