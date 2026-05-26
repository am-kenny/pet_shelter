import datetime

from animals.scheduling.defaults import (
    DEFAULT_SHELTER_CLOSE,
    DEFAULT_SHELTER_OPEN,
    DEFAULT_SLOT_STEP_MINUTES,
)
from animals.scheduling.types import BookingScheduleContext, ShelterDayHours


def resolve_shelter_hours(for_date: datetime.date) -> ShelterDayHours | None:
    """Return open/close for for_date, or None when the shelter is closed.

    Order: date override, weekday row, then ``DEFAULT_SHELTER_*``. An override
    with only one of ``opens_at`` / ``closes_at`` falls through; an open weekday
    row with missing times uses the same defaults.
    """
    from animals.models import ShelterDateOverride, ShelterWeekdayHours

    override = ShelterDateOverride.objects.filter(calendar_date=for_date).first()
    if override is not None:
        if override.is_closed:
            return None
        if override.opens_at is not None and override.closes_at is not None:
            return ShelterDayHours(override.opens_at, override.closes_at)

    weekday = ShelterWeekdayHours.objects.filter(weekday=for_date.weekday()).first()
    if weekday is not None:
        if weekday.is_closed:
            return None
        if weekday.opens_at is not None and weekday.closes_at is not None:
            return ShelterDayHours(weekday.opens_at, weekday.closes_at)

    return ShelterDayHours(DEFAULT_SHELTER_OPEN, DEFAULT_SHELTER_CLOSE)


def get_slot_step() -> datetime.timedelta:
    from animals.models import ShelterBookingSettings

    minutes = max(1, ShelterBookingSettings.load().slot_step_minutes)
    return datetime.timedelta(minutes=minutes)


def load_schedule_context(for_date: datetime.date) -> BookingScheduleContext:
    """Hours and slot step for for_date (up to ~3 queries; one if closed)."""
    hours = resolve_shelter_hours(for_date)
    slot_step = (
        get_slot_step()
        if hours is not None
        else datetime.timedelta(minutes=DEFAULT_SLOT_STEP_MINUTES)
    )
    return BookingScheduleContext(
        for_date=for_date,
        hours=hours,
        slot_step=slot_step,
    )
