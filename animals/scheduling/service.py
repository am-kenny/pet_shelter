import datetime

from animals.scheduling.availability import available_booking_times
from animals.scheduling.hours import load_schedule_context
from animals.scheduling.types import Timeslot


def timeslots_from_schedule(rows) -> list[Timeslot]:
    return [Timeslot(row.start_time, row.end_time) for row in rows]


def available_slots_for_day(
    animal_schedule,
    booking_date: str,
    duration_hours: int | float,
    duration_minutes: int,
) -> list[str]:
    """Booked rows for one animal/day → offered HH:MM start times."""
    booked_slots = timeslots_from_schedule(animal_schedule)
    for_date = datetime.date.fromisoformat(booking_date)
    schedule = load_schedule_context(for_date)
    return available_booking_times(
        booked_slots,
        duration_hours,
        duration_minutes,
        for_date=for_date,
        schedule=schedule,
    )
