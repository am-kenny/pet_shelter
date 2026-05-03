import datetime

from django.utils import timezone as dj_timezone

# TODO: make configurable from the database
shelter_open_time = datetime.time(8, 0)  # Pet shelter open time
shelter_close_time = datetime.time(18, 0)  # Pet shelter close time


def _ensure_aware(dt: datetime.datetime) -> datetime.datetime:
    if dj_timezone.is_naive(dt):
        return dj_timezone.make_aware(dt, dj_timezone.get_current_timezone())
    return dt


def sort_times(booked_times: list[tuple]) -> list[tuple]:
    """
    Sort a list of tuples based on the first element of each tuple in ascending order.

    :param booked_times: A list of tuples containing time information.
    :type booked_times: list[tuple]

    :return: A sorted list of tuples based on the first element of each tuple.
    :rtype: list[tuple]
    """
    sorted_times = sorted(booked_times, key=lambda x: x[0])

    return sorted_times


def available_time_periods(
    booked_times: list[tuple[datetime.datetime, datetime.datetime]],
) -> list[list[datetime.datetime]]:
    """
    Calculate and return a list of free time periods based on the booked times.

    :param booked_times: A list of tuples, where each tuple represents a booked time period.
                         Each tuple should contain two datetime objects, indicating the start and end times.
    :type booked_times: List[Tuple[datetime.datetime, datetime.datetime]]

    :return: A list of free time periods represented as tuples of datetime objects, where each tuple
             contains the start and end times of a free period.
    :rtype: List[List[datetime.datetime]]
    """
    # Sort the input list of booked times
    booked_times = sort_times(booked_times)

    # Initialize a list to store free time periods
    if booked_times:
        free_time: list[list] = [[None] * 2 for _ in range(0, len(booked_times) + 1)]
        for i in range(0, len(booked_times)):
            free_time[i][1] = booked_times[i][0]
            free_time[i + 1][0] = booked_times[i][1]
        day = booked_times[0][0].date()
        tz = (
            booked_times[0][0].tzinfo
            if dj_timezone.is_aware(booked_times[0][0])
            else dj_timezone.get_current_timezone()
        )
        free_time[0][0] = dj_timezone.make_aware(
            datetime.datetime.combine(day, shelter_open_time), tz
        )
        free_time[-1][1] = dj_timezone.make_aware(
            datetime.datetime.combine(day, shelter_close_time), tz
        )
    else:
        today = dj_timezone.now().date()
        free_time = [
            [
                _ensure_aware(datetime.datetime.combine(today, shelter_open_time)),
                _ensure_aware(datetime.datetime.combine(today, shelter_close_time)),
            ]
        ]

    return free_time


def available_booking_times(
    booked_times: list[tuple[datetime.datetime, datetime.datetime]],
    duration_hours: int | float,
    duration_minutes: int,
) -> list[str]:
    """
    Calculate and return a list of available booking times based on booked times and desired duration.

    :param booked_times: A list of tuples, where each tuple represents a booked time period.
                         Each tuple should contain two datetime objects, indicating the start and end times.
    :type booked_times: List[Tuple[datetime.datetime, datetime.datetime]]

    :param duration_hours: The desired duration for available booking times in hours (int or float).
    :type duration_hours: int | float

    :param duration_minutes: The desired duration for available booking times in minutes (int).
    :type duration_minutes: int

    :return: A list of available booking times in "HH:MM" format that meet the requested duration.
    :rtype: List[str]
    """

    # Calculate free time periods based on booked times
    free_time = available_time_periods(booked_times)

    # Convert the desired duration to a timedelta object
    duration = datetime.timedelta(hours=duration_hours, minutes=duration_minutes)

    # Create a list of available booking times
    available_times = []
    for period in free_time:
        current_time = period[0]
        while current_time < period[1]:
            if current_time + duration <= period[1]:
                available_times.append(current_time.strftime("%H:%M"))
            current_time = current_time + datetime.timedelta(minutes=15)

    return available_times


def create_booked_time(
    booking_date: str,
    time_slot: str,
    duration_hours: str | int | float,
    duration_minutes: str | int = 0,
) -> tuple[datetime.datetime, datetime.datetime]:
    """
    Create a booked time slot based on a booking date, time slot, and duration.

    :param booking_date: The booking date in "YYYY-MM-DD" format.
    :type booking_date: str

    :param time_slot: The time slot in "HH:MM" format.
    :type time_slot: str

    :param duration_hours: The duration in hours (str).
    :type duration_hours: str | int | float

    :param duration_minutes: The duration in minutes (str).
    :type duration_minutes: str | int

    :return: A tuple containing the booking start and end times as datetime objects.
    :rtype: tuple[datetime.datetime, datetime.datetime]
    """

    try:
        # Parse the input date and time
        booking_date = datetime.datetime.strptime(booking_date, "%Y-%m-%d")
        booking_time = datetime.datetime.strptime(time_slot, "%H:%M").time()
    except ValueError as err:
        raise ValueError("Invalid date or time format") from err

    # Combine date and time to get the booking start time
    booking_start = _ensure_aware(
        datetime.datetime.combine(booking_date.date(), booking_time)
    )

    # Convert the duration to numerical types
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

    # Convert the duration to a timedelta
    duration = datetime.timedelta(hours=duration_hours, minutes=duration_minutes)

    # Calculate the booking end time
    booking_end = booking_start + duration

    return booking_start, booking_end
