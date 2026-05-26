import datetime

from django.utils import timezone as dj_timezone

from animals.scheduling.hours import load_schedule_context, resolve_shelter_hours
from animals.scheduling.types import BookingScheduleContext, ShelterDayHours, Timeslot


def sort_times(booked_slots: list[Timeslot]) -> list[Timeslot]:
    return sorted(booked_slots, key=lambda slot: slot.start)


def _shelter_bounds(
    for_date: datetime.date,
    tz: datetime.tzinfo,
    hours: ShelterDayHours,
) -> tuple[datetime.datetime, datetime.datetime]:
    open_dt = dj_timezone.make_aware(
        datetime.datetime.combine(for_date, hours.opens_at), tz
    )
    close_dt = dj_timezone.make_aware(
        datetime.datetime.combine(for_date, hours.closes_at), tz
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
    schedule: BookingScheduleContext | None = None,
) -> list[Timeslot]:
    """Free gaps on for_date between shelter hours and booked slots.

    Slots are sorted by start; overlaps are not merged. Zero-length gaps omitted.
    Optional ``schedule`` avoids re-querying (``hours is None`` means closed).
    """
    if schedule is not None:
        if schedule.for_date != for_date:
            raise ValueError("schedule.for_date must match for_date")
        hours = schedule.hours
    else:
        hours = resolve_shelter_hours(for_date)
    if hours is None:
        return []

    if not booked_slots:
        open_dt, close_dt = _shelter_bounds(
            for_date, dj_timezone.get_current_timezone(), hours
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
    open_dt, close_dt = _shelter_bounds(for_date, tz, hours)

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
    schedule: BookingScheduleContext | None = None,
) -> list[str]:
    """HH:MM start times that fit in a free period for the requested duration.

    Pass ``schedule`` from :func:`load_schedule_context` to cache DB resolution.
    """
    ctx = schedule or load_schedule_context(for_date)
    if ctx.for_date != for_date:
        raise ValueError("schedule.for_date must match for_date")

    free_time = available_time_periods(booked_slots, for_date=for_date, schedule=ctx)
    duration = datetime.timedelta(hours=duration_hours, minutes=duration_minutes)
    slot_step = ctx.slot_step

    available_times: list[str] = []
    for period in free_time:
        current_time = period.start
        while current_time < period.end:
            if current_time + duration <= period.end:
                available_times.append(current_time.strftime("%H:%M"))
            current_time += slot_step

    return available_times
