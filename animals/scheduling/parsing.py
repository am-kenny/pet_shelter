import datetime

from django.utils import timezone as dj_timezone

from animals.scheduling.types import Timeslot


def _ensure_aware(dt: datetime.datetime) -> datetime.datetime:
    if dj_timezone.is_naive(dt):
        return dj_timezone.make_aware(dt, dj_timezone.get_current_timezone())
    return dt


def create_booked_time(
    booking_date: str,
    time_slot: str,
    duration_hours: str | int | float,
    duration_minutes: str | int = 0,
) -> Timeslot:
    """Parse form inputs and return the booked walk as a Timeslot."""
    try:
        parsed_date = datetime.datetime.strptime(booking_date, "%Y-%m-%d")
        parsed_time = datetime.datetime.strptime(time_slot, "%H:%M").time()
    except ValueError as err:
        raise ValueError("Invalid date or time format") from err

    booking_start = _ensure_aware(
        datetime.datetime.combine(parsed_date.date(), parsed_time)
    )

    if isinstance(duration_hours, str):
        try:
            duration_hours = float(duration_hours)
        except ValueError as err:
            raise ValueError("Invalid hours duration format") from err
    if isinstance(duration_minutes, str):
        try:
            duration_minutes = int(duration_minutes)
        except ValueError as err:
            raise ValueError("Invalid minutes duration format") from err

    duration = datetime.timedelta(hours=duration_hours, minutes=duration_minutes)
    return Timeslot(booking_start, booking_start + duration)
