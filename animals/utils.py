from typing import List, Tuple  # imported typing to remove type warnings
import datetime

shelter_open_time = datetime.time(8, 0)  # Pet shelter open time
shelter_close_time = datetime.time(18, 0)  # Pet shelter close time


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


def available_time_periods(booked_times: List[Tuple[datetime.datetime, datetime.datetime]]
                           ) -> List[List[datetime.datetime]]:
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
        free_time: List[List] = [[None] * 2 for _ in range(0, len(booked_times) + 1)]
        for i in range(0, len(booked_times)):
            free_time[i][1] = booked_times[i][0]
            free_time[i + 1][0] = booked_times[i][1]
        free_time[0][0] = datetime.datetime.combine(booked_times[0][0].date(), shelter_open_time)
        free_time[-1][1] = datetime.datetime.combine(booked_times[0][0].date(), shelter_close_time)
    else:
        free_time = [[datetime.datetime.combine(datetime.date.today(), shelter_open_time),
                     datetime.datetime.combine(datetime.date.today(), shelter_close_time)]]

    return free_time


def available_booking_times(booked_times: List[Tuple[datetime.datetime, datetime.datetime]],
                            duration_hours: int | float,
                            duration_minutes: int) -> List[str]:
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


def create_booked_time(booking_date: str,
                       time_slot: str,
                       duration_hours: str | int | float,
                       duration_minutes: str | int = 0) -> (datetime.datetime, datetime.datetime):
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
    :rtype: (datetime, datetime)
    """

    try:
        # Parse the input date and time
        booking_date = datetime.datetime.strptime(booking_date, "%Y-%m-%d")
        booking_time = datetime.datetime.strptime(time_slot, "%H:%M").time()
    except ValueError:
        raise ValueError("Invalid date or time format")

    # Combine date and time to get the booking start time
    booking_start = datetime.datetime.combine(booking_date, booking_time)

    # Convert the duration to numerical types
    if isinstance(duration_hours, str):
        try:
            duration_hours = float(duration_hours)
        except ValueError:
            raise ValueError("Invalid hours duration format")
    if isinstance(duration_minutes, str):
        try:
            duration_minutes = int(duration_minutes)
        except ValueError:
            raise ValueError("Invalid minutes duration format")

    # Convert the duration to a timedelta
    duration = datetime.timedelta(hours=duration_hours, minutes=duration_minutes)

    # Calculate the booking end time
    booking_end = booking_start + duration

    return booking_start, booking_end
