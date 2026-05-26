from django.contrib import admin

# Register your models here.
from animals import models

admin.site.register(models.Animal)
admin.site.register(models.Sex)
admin.site.register(models.Schedule)
admin.site.register(models.AnimalMedia)
admin.site.register(models.ShelterWeekdayHours)
admin.site.register(models.ShelterDateOverride)


@admin.register(models.ShelterBookingSettings)
class ShelterBookingSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not models.ShelterBookingSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
