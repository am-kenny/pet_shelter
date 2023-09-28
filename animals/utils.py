from typing import List  # imported typing to remove type warnings
import datetime

shelter_open_time = datetime.time(8, 0)  # Pet shelter open time
shelter_close_time = datetime.time(18, 0)  # Pet shelter close time


def sort_times(booked_times: list[tuple]):
    sorted_times = sorted(booked_times, key=lambda x: x[0])
    return sorted_times


def available_time_periods(booked_times: list[tuple]):
    booked_times = sort_times(booked_times)
    # create new list of free time periods
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


def available_booking_times(booked_times: list[tuple],
                            duration_hours: int | float,
                            duration_minutes: int):

    free_time = available_time_periods(booked_times)

    # set desired duration to timedelta object
    duration = datetime.timedelta(hours=duration_hours, minutes=duration_minutes)

    # create new list of available times which meet requested duration
    available_times = []
    for period in free_time:
        current_time = period[0]
        while current_time < period[1]:
            if current_time + duration <= period[1]:
                available_times.append(current_time.strftime("%H:%M"))
            current_time = current_time + datetime.timedelta(minutes=15)
    return available_times
