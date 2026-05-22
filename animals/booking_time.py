import datetime
from dataclasses import dataclass

from django.utils import timezone as dj_timezone

# TODO: make configurable from the database
shelter_open_time = datetime.time(8, 0)
shelter_close_time = datetime.time(18, 0)
slot_step = datetime.timedelta(minutes=15)


@dataclass(frozen=True)
class Timeslot:
    start: datetime.datetime
    end: datetime.datetime

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError("Timeslot start must be before end")


def _ensure_aware(dt: datetime.datetime) -> datetime.datetime:
    if dj_timezone.is_naive(dt):
        return dj_timezone.make_aware(dt, dj_timezone.get_current_timezone())
    return dt


def sort_times(booked_slots: list[Timeslot]) -> list[Timeslot]:
    """Return booked slots sorted by start time ascending."""
    return sorted(booked_slots, key=lambda slot: slot.start)


def _shelter_bounds(
    for_date: datetime.date,
    tz: datetime.tzinfo,
) -> tuple[datetime.datetime, datetime.datetime]:
    open_dt = dj_timezone.make_aware(
        datetime.datetime.combine(for_date, shelter_open_time), tz
    )
    close_dt = dj_timezone.make_aware(
        datetime.datetime.combine(for_date, shelter_close_time), tz
    )
    return open_dt, close_dt


def _append_free_period(
    free_time: list[Timeslot], start: datetime.datetime, end: datetime.datetime
) -> None:
    if start < end:
        free_time.append(Timeslot(start, end))


def available_time_periods(
    booked_slots: list[Timeslot],
    *,
    for_date: datetime.date,
) -> list[Timeslot]:
    """Return free gaps on for_date between shelter hours and booked slots.

    Booked slots should fall on for_date; they are sorted by start time only
    (overlaps are not merged). Gaps with start >= end are omitted.
    """
    if not booked_slots:
        open_dt, close_dt = _shelter_bounds(
            for_date, dj_timezone.get_current_timezone()
        )
        free_time: list[Timeslot] = []
        _append_free_period(free_time, open_dt, close_dt)
        return free_time

    booked_slots = sort_times(booked_slots)
    tz = (
        booked_slots[0].start.tzinfo
        if dj_timezone.is_aware(booked_slots[0].start)
        else dj_timezone.get_current_timezone()
    )
    open_dt, close_dt = _shelter_bounds(for_date, tz)

    free_time = []
    prev_end = open_dt
    for booked in booked_slots:
        _append_free_period(free_time, prev_end, booked.start)
        prev_end = booked.end
    _append_free_period(free_time, prev_end, close_dt)
    return free_time


def available_booking_times(
    booked_slots: list[Timeslot],
    duration_hours: int | float,
    duration_minutes: int,
    *,
    for_date: datetime.date,
) -> list[str]:
    """Return HH:MM start times that fit in a free period for the given duration."""
    free_time = available_time_periods(booked_slots, for_date=for_date)
    duration = datetime.timedelta(hours=duration_hours, minutes=duration_minutes)

    available_times: list[str] = []
    for period in free_time:
        current_time = period.start
        while current_time < period.end:
            if current_time + duration <= period.end:
                available_times.append(current_time.strftime("%H:%M"))
            current_time += slot_step

    return available_times


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
