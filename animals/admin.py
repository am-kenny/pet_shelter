from django.contrib import admin

# Register your models here.
from animals import models

admin.site.register(models.Animal)
admin.site.register(models.Sex)
admin.site.register(models.Schedule)
admin.site.register(models.AnimalMedia)
