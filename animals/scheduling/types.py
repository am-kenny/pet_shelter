import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class ShelterDayHours:
    opens_at: datetime.time
    closes_at: datetime.time


@dataclass(frozen=True)
class Timeslot:
    start: datetime.datetime
    end: datetime.datetime

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError("Timeslot start must be before end")


@dataclass(frozen=True)
class BookingScheduleContext:
    for_date: datetime.date
    hours: ShelterDayHours | None
    slot_step: datetime.timedelta
