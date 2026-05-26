from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from animals.scheduling.defaults import DEFAULT_SLOT_STEP_MINUTES
from pet_shelter import settings


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
    media = models.ImageField(blank=False, upload_to="animal_images/", unique=True)
    is_main = models.BooleanField()

    def __str__(self):
        return f"AnimalMedia({self.animal_id}, main={self.is_main})"


class Schedule(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return f"Schedule({self.start_time} - {self.end_time}, animal={self.animal_id})"

    @property
    def is_past_due(self):
        return timezone.now() > self.start_time

    @classmethod
    def user_has_completed_walk(cls, user, animal_id: int) -> bool:
        """True if this user had a booking with the animal whose slot has fully ended."""
        if not getattr(user, "is_authenticated", False):
            return False
        return cls.objects.filter(
            user=user,
            animal_id=animal_id,
            end_time__lt=timezone.now(),
        ).exists()


class ShelterWeekdayHours(models.Model):
    """Opening hours for one weekday; aligns with ``datetime.date.weekday()`` (Monday=0)."""

    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"

    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices, unique=True)
    is_closed = models.BooleanField(
        default=False,
        help_text="When checked, no visits are offered on this day.",
    )
    opens_at = models.TimeField(null=True, blank=True)
    closes_at = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ["weekday"]
        verbose_name = "shelter weekday hours"
        verbose_name_plural = "shelter weekday hours"

    def __str__(self):
        if self.is_closed:
            return f"{self.get_weekday_display()}: closed"
        return f"{self.get_weekday_display()}: {self.opens_at}–{self.closes_at}"

    def clean(self):
        super().clean()
        if self.is_closed:
            return
        if self.opens_at is None or self.closes_at is None:
            raise ValidationError(
                "Open days must have both opening and closing times set."
            )
        if self.opens_at >= self.closes_at:
            raise ValidationError("Closing time must be after opening time.")


class ShelterDateOverride(models.Model):
    """Hours for a single calendar day; overrides ``ShelterWeekdayHours`` when present."""

    calendar_date = models.DateField(unique=True, db_index=True)
    is_closed = models.BooleanField(
        default=False,
        help_text="When checked, no visits on this date (e.g. holiday).",
    )
    opens_at = models.TimeField(null=True, blank=True)
    closes_at = models.TimeField(null=True, blank=True)
    reason = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional note (e.g. holiday name).",
    )

    class Meta:
        ordering = ["calendar_date"]
        verbose_name = "shelter date override"
        verbose_name_plural = "shelter date overrides"

    def __str__(self):
        label = self.calendar_date.isoformat()
        if self.reason:
            label = f"{label} ({self.reason})"
        if self.is_closed:
            return f"{label}: closed"
        return f"{label}: {self.opens_at}–{self.closes_at}"

    def clean(self):
        super().clean()
        if self.is_closed:
            return
        if self.opens_at is None or self.closes_at is None:
            raise ValidationError(
                "Open days must have both opening and closing times set."
            )
        if self.opens_at >= self.closes_at:
            raise ValidationError("Closing time must be after opening time.")


class ShelterBookingSettings(models.Model):
    """Singleton settings for visit scheduling (one row, pk=1)."""

    slot_step_minutes = models.PositiveSmallIntegerField(
        default=DEFAULT_SLOT_STEP_MINUTES,
        validators=[MinValueValidator(1)],
        help_text="Minutes between offered start times in the slot picker.",
    )

    class Meta:
        verbose_name = "shelter booking settings"
        verbose_name_plural = "shelter booking settings"

    def __str__(self):
        return f"Booking settings (slot step: {self.slot_step_minutes} min)"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> ShelterBookingSettings:
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
