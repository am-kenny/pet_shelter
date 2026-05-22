import datetime
import unittest

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

import animals.models
from animals.booking_time import (
    Timeslot,
    available_booking_times,
    available_time_periods,
    create_booked_time,
    sort_times,
)


def _utc(*parts):
    """UTC-aware datetime for tests (year..hour, optional minute, second)."""
    y, mo, d, h, *rest = (*parts, 0, 0)
    return datetime.datetime(y, mo, d, h, rest[0], rest[1], tzinfo=datetime.UTC)


def _d(year, month, day):
    return datetime.date(year, month, day)


def _slot(start, end):
    return Timeslot(start, end)


# Schedule testing
class TestScheduleSortedPeriods(TestCase):
    def test_schedule_1(self):
        expected = [
            "08:00",
            "08:15",
            "08:30",
            "08:45",
            "09:00",
            "09:15",
            "09:30",
            "12:00",
            "12:15",
            "12:30",
            "16:00",
            "16:15",
            "16:30",
        ]
        booked = [
            _slot(
                _utc(2023, 9, 12, 11, 0),
                _utc(2023, 9, 12, 12, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 14, 0),
                _utc(2023, 9, 12, 16, 0),
            ),
        ]
        hours = 1
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_2(self):
        expected = [
            "08:00",
            "08:15",
            "08:30",
            "08:45",
            "09:00",
            "09:15",
            "09:30",
            "14:00",
            "14:15",
            "14:30",
            "14:45",
            "15:00",
            "15:15",
            "15:30",
            "15:45",
            "16:00",
            "16:15",
            "16:30",
        ]
        booked = [
            _slot(
                _utc(2023, 9, 12, 11, 0),
                _utc(2023, 9, 12, 12, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 12, 0),
                _utc(2023, 9, 12, 14, 0),
            ),
        ]
        hours = 1
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_3(self):
        expected = [
            "08:00",
            "08:15",
            "08:30",
            "08:45",
            "09:00",
            "09:15",
            "09:30",
            "14:00",
            "14:15",
            "14:30",
            "14:45",
            "15:00",
            "15:15",
            "15:30",
            "15:45",
            "16:00",
            "16:15",
            "16:30",
        ]
        booked = [
            _slot(
                _utc(2024, 1, 15, 11, 0),
                _utc(2024, 1, 15, 12, 0),
            ),
            _slot(
                _utc(2024, 1, 15, 12, 0),
                _utc(2024, 1, 15, 14, 0),
            ),
        ]
        hours = 1
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2024, 1, 15)
        )
        self.assertEqual(result, expected)

    def test_schedule_4(self):
        expected = [
            "09:00",
            "09:15",
            "09:30",
            "09:45",
            "10:00",
            "10:15",
            "10:30",
            "14:00",
            "14:15",
            "14:30",
            "14:45",
            "15:00",
            "15:15",
            "15:30",
            "15:45",
            "16:00",
            "16:15",
            "16:30",
        ]
        booked = [
            _slot(
                _utc(2023, 9, 12, 8, 0),
                _utc(2023, 9, 12, 9, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 12, 0),
                _utc(2023, 9, 12, 14, 0),
            ),
        ]
        hours = 1
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_5(self):
        expected = []
        booked = [
            _slot(
                _utc(2023, 9, 12, 8, 0),
                _utc(2023, 9, 12, 9, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 10, 0),
                _utc(2023, 9, 12, 14, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 15, 0),
                _utc(2023, 9, 12, 17, 0),
            ),
        ]
        hours = 1
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_6(self):
        expected = [
            "09:00",
            "09:15",
            "09:30",
            "09:45",
            "14:30",
            "14:45",
            "17:00",
            "17:15",
            "17:30",
            "17:45",
        ]
        booked = [
            _slot(
                _utc(2023, 9, 12, 8, 0),
                _utc(2023, 9, 12, 9, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 10, 0),
                _utc(2023, 9, 12, 14, 30),
            ),
            _slot(
                _utc(2023, 9, 12, 15, 0),
                _utc(2023, 9, 12, 17, 0),
            ),
        ]
        hours = 0
        minutes = 15
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)


class TestScheduleUnsortedPeriods(unittest.TestCase):
    def test_schedule_1(self):
        expected = ["15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30"]
        booked = [
            _slot(
                _utc(2023, 9, 12, 13, 0),
                _utc(2023, 9, 12, 14, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 11, 0),
                _utc(2023, 9, 12, 12, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 14, 0),
                _utc(2023, 9, 12, 15, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 9, 0),
                _utc(2023, 9, 12, 10, 0),
            ),
        ]
        hours = 1
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_2(self):
        expected = [
            "14:00",
            "14:15",
            "14:30",
            "14:45",
            "15:00",
            "15:15",
            "15:30",
            "15:45",
            "16:00",
            "16:15",
            "16:30",
        ]
        booked = [
            _slot(
                _utc(2023, 9, 12, 13, 0),
                _utc(2023, 9, 12, 14, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 11, 0),
                _utc(2023, 9, 12, 12, 0),
            ),
            _slot(
                _utc(2023, 9, 12, 9, 0),
                _utc(2023, 9, 12, 10, 0),
            ),
        ]
        hours = 1
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_3(self):
        expected = ["15:00", "15:15"]
        booked = [
            _slot(
                _utc(2023, 12, 18, 13, 0),
                _utc(2023, 12, 18, 14, 0),
            ),
            _slot(
                _utc(2023, 12, 18, 11, 0),
                _utc(2023, 12, 18, 12, 0),
            ),
            _slot(
                _utc(2023, 12, 18, 14, 0),
                _utc(2023, 12, 18, 15, 0),
            ),
            _slot(
                _utc(2023, 12, 18, 9, 0),
                _utc(2023, 12, 18, 10, 0),
            ),
        ]
        hours = 2
        minutes = 45
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 12, 18)
        )
        self.assertEqual(result, expected)


class TestScheduleEmpty(unittest.TestCase):
    def test_schedule_1(self):
        expected = [
            "08:00",
            "08:15",
            "08:30",
            "08:45",
            "09:00",
            "09:15",
            "09:30",
            "09:45",
            "10:00",
            "10:15",
            "10:30",
            "10:45",
            "11:00",
            "11:15",
            "11:30",
            "11:45",
            "12:00",
            "12:15",
            "12:30",
            "12:45",
            "13:00",
            "13:15",
            "13:30",
            "13:45",
            "14:00",
            "14:15",
            "14:30",
            "14:45",
            "15:00",
            "15:15",
            "15:30",
            "15:45",
            "16:00",
            "16:15",
            "16:30",
        ]
        booked = []
        hours = 1
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_2(self):
        expected = [
            "08:00",
            "08:15",
            "08:30",
            "08:45",
            "09:00",
            "09:15",
            "09:30",
            "09:45",
            "10:00",
            "10:15",
            "10:30",
            "10:45",
            "11:00",
            "11:15",
            "11:30",
            "11:45",
            "12:00",
            "12:15",
            "12:30",
            "12:45",
            "13:00",
            "13:15",
            "13:30",
            "13:45",
            "14:00",
            "14:15",
            "14:30",
            "14:45",
            "15:00",
            "15:15",
            "15:30",
            "15:45",
            "16:00",
            "16:15",
            "16:30",
            "16:45",
            "17:00",
            "17:15",
            "17:30",
        ]
        booked = []
        hours = 0
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_4(self):
        expected = ["08:00", "08:15", "08:30"]
        booked = []
        hours = 9
        minutes = 30
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_5(self):
        expected = [
            "08:00",
            "08:15",
            "08:30",
            "08:45",
            "09:00",
            "09:15",
            "09:30",
            "09:45",
            "10:00",
            "10:15",
            "10:30",
            "10:45",
            "11:00",
            "11:15",
            "11:30",
            "11:45",
            "12:00",
            "12:15",
            "12:30",
            "12:45",
            "13:00",
            "13:15",
            "13:30",
            "13:45",
            "14:00",
            "14:15",
            "14:30",
            "14:45",
            "15:00",
            "15:15",
            "15:30",
            "15:45",
            "16:00",
            "16:15",
            "16:30",
            "16:45",
            "17:00",
            "17:15",
            "17:30",
            "17:45",
        ]
        booked = []
        hours = 0
        minutes = 15
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_one_available(self):
        expected = ["08:00"]
        booked = []
        hours = 10
        minutes = 0
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)

    def test_schedule_no_available(self):
        expected = []
        booked = []
        hours = 10
        minutes = 15
        result = available_booking_times(
            booked, hours, minutes, for_date=_d(2023, 9, 12)
        )
        self.assertEqual(result, expected)


class TestBookingTime(unittest.TestCase):
    def test_sort_times_orders_by_start(self):
        slots = [
            _slot(_utc(2023, 9, 12, 14, 0), _utc(2023, 9, 12, 15, 0)),
            _slot(_utc(2023, 9, 12, 9, 0), _utc(2023, 9, 12, 10, 0)),
            _slot(_utc(2023, 9, 12, 11, 0), _utc(2023, 9, 12, 12, 0)),
        ]
        sorted_slots = sort_times(slots)
        self.assertEqual(
            [s.start.hour for s in sorted_slots],
            [9, 11, 14],
        )

    def test_available_time_periods_empty_uses_for_date(self):
        day = _d(2030, 1, 5)
        free = available_time_periods([], for_date=day)
        self.assertEqual(free[0].start.date(), day)
        self.assertEqual(free[0].end.date(), day)

    def test_available_time_periods_between_bookings(self):
        booked = [
            _slot(_utc(2023, 9, 12, 11, 0), _utc(2023, 9, 12, 12, 0)),
            _slot(_utc(2023, 9, 12, 14, 0), _utc(2023, 9, 12, 16, 0)),
        ]
        free = available_time_periods(booked, for_date=_d(2023, 9, 12))
        self.assertEqual(len(free), 3)
        self.assertEqual(free[0].start.strftime("%H:%M"), "08:00")
        self.assertEqual(free[0].end.strftime("%H:%M"), "11:00")
        self.assertEqual(free[1].start.strftime("%H:%M"), "12:00")
        self.assertEqual(free[1].end.strftime("%H:%M"), "14:00")
        self.assertEqual(free[2].start.strftime("%H:%M"), "16:00")
        self.assertEqual(free[2].end.strftime("%H:%M"), "18:00")

    def test_available_time_periods_skips_zero_length_gaps(self):
        booked = [
            _slot(_utc(2023, 9, 12, 10, 0), _utc(2023, 9, 12, 12, 0)),
            _slot(_utc(2023, 9, 12, 12, 0), _utc(2023, 9, 12, 14, 0)),
        ]
        free = available_time_periods(booked, for_date=_d(2023, 9, 12))
        self.assertEqual(len(free), 2)
        self.assertEqual(free[0].end.strftime("%H:%M"), "10:00")
        self.assertEqual(free[1].start.strftime("%H:%M"), "14:00")

    def test_timeslot_rejects_invalid_range(self):
        with self.assertRaises(ValueError):
            _slot(_utc(2023, 9, 12, 12, 0), _utc(2023, 9, 12, 11, 0))

    def test_create_booked_time(self):
        slot = create_booked_time("2023-09-12", "10:30", 1, 30)
        self.assertEqual(slot.start.strftime("%Y-%m-%d %H:%M"), "2023-09-12 10:30")
        self.assertEqual(slot.end.strftime("%Y-%m-%d %H:%M"), "2023-09-12 12:00")

    def test_create_booked_time_parses_string_duration(self):
        slot = create_booked_time("2023-09-12", "10:30", "1", "30")
        self.assertEqual(slot.end - slot.start, datetime.timedelta(hours=1, minutes=30))

    def test_create_booked_time_invalid_date(self):
        with self.assertRaises(ValueError):
            create_booked_time("not-a-date", "10:30", 1, 0)

    def test_create_booked_time_invalid_duration(self):
        with self.assertRaises(ValueError):
            create_booked_time("2023-09-12", "10:30", "x", 0)


# Endpoints testing
class TestAnimals(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        self.test_animal = animals.models.Animal.objects.filter(id=3).first()

    def test_animals_page(self):
        test_client = Client()
        response = test_client.get("/animals")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_animal_page(self):
        test_client = Client()
        response = test_client.get(reverse("animal", args=[self.test_animal.id]))
        status_code = response.status_code
        has_animal_name = self.test_animal.name in response.content.decode("utf-8")
        self.assertEqual(status_code, 200)
        self.assertTrue(has_animal_name)

    def test_animal_page_fail(self):  # Unexisting animal
        test_client = Client()
        response = test_client.get(reverse("animal", args=[777]))
        status_code = response.status_code
        self.assertEqual(status_code, 404)

    def test_animal_page_feedback_after_completed_walk(self):
        test_client = Client()
        user = get_user_model().objects.get(username="guest")
        test_client.force_login(user)
        response = test_client.get(reverse("animal", args=[1]))
        self.assertEqual(response.status_code, 200)
        body = response.content.decode("utf-8")
        self.assertIn("Leave feedback", body)

    def test_animal_page_feedback_hint_without_completed_walk(self):
        test_client = Client()
        user = get_user_model().objects.get(username="guest")
        test_client.force_login(user)
        response = test_client.get(reverse("animal", args=[2]))
        self.assertEqual(response.status_code, 200)
        body = response.content.decode("utf-8")
        self.assertNotIn("Leave feedback", body)
        self.assertIn("Feedback opens here after", body)


class TestAnimalSchedule(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        self.test_animal = animals.models.Animal.objects.filter(id=3).first()

    @staticmethod
    def logged_client():
        test_client = Client()
        user = get_user_model().objects.get(username="guest")
        test_client.force_login(user)
        return test_client

    def test_schedule_get_1(self):
        test_client = self.logged_client()
        response = test_client.get("/schedule")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_schedule_get_2(self):
        test_client = self.logged_client()
        response = test_client.get(
            "/schedule",
            data={
                "animal_id": self.test_animal.id,
                "date": "2023-10-14",
                "duration_hours": 1,
                "duration_minutes": 0,
            },
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        body = response.content.decode("utf-8")
        self.assertNotIn("schedule-available-timeslots", body)

    def test_schedule_post_filter_renders_slots(self):
        test_client = self.logged_client()
        response = test_client.post(
            "/schedule",
            data={
                "animal_id": self.test_animal.id,
                "selected_date": "2023-10-14",
                "duration_hours": 1,
                "duration_minutes": 0,
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.content.decode("utf-8")
        self.assertIn("schedule-available-timeslots", body)
        self.assertIn("Available time slots", body)

    def test_schedule_get_3(self):
        test_client = Client()
        response = test_client.get("/schedule")
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_schedule_get_4(self):  # Test exception handling
        test_client = self.logged_client()
        response = test_client.get(
            "/schedule",
            data={
                "animal_id": self.test_animal.id,
                "date": "2023-10-14",
                "duration_hours": "some bad data",
                "duration_minutes": "some bad data",
            },
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_schedule_get_fail(self):  # Unexisting animal
        test_client = self.logged_client()
        response = test_client.get(
            "/schedule",
            data={
                "animal_id": 777,
                "date": "2023-10-13",
                "duration_hours": 1,
                "duration_minutes": 0,
            },
        )
        status_code = response.status_code
        self.assertEqual(status_code, 404)

    def test_schedule_post(self):
        test_client = self.logged_client()
        slot_payload = {
            "animal_id": self.test_animal.id,
            "selected_slot": "10:00",
            "selected_date": "2023-12-14",
            "duration_hours": 1,
            "duration_minutes": 0,
        }
        preview = test_client.post("/schedule", data=slot_payload)
        self.assertEqual(preview.status_code, 200)
        self.assertTemplateUsed(preview, "animals/schedule_confirm.html")
        self.assertFalse(
            animals.models.Schedule.objects.filter(
                start_time=_utc(2023, 12, 14, 10)
            ).exists()
        )

        response = test_client.post(
            "/schedule",
            data={**slot_payload, "confirm_schedule": "1"},
        )
        status_code = response.status_code
        test_schedule = animals.models.Schedule.objects.get(
            start_time=_utc(2023, 12, 14, 10)
        )

        self.assertEqual(test_schedule.start_time, _utc(2023, 12, 14, 10, 0))
        self.assertEqual(test_schedule.end_time, _utc(2023, 12, 14, 11, 0))
        self.assertEqual(test_schedule.user_id, 4)
        self.assertEqual(test_schedule.animal_id, self.test_animal.id)
        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response, "animals/success.html")

    def test_schedule_post_2(self):  # At the start of the working day
        test_client = self.logged_client()
        slot_payload = {
            "animal_id": self.test_animal.id,
            "selected_slot": "08:00",
            "selected_date": "2023-12-25",
            "duration_hours": 3,
            "duration_minutes": 0,
        }
        test_client.post("/schedule", data=slot_payload)
        response = test_client.post(
            "/schedule",
            data={**slot_payload, "confirm_schedule": "1"},
        )
        status_code = response.status_code
        test_schedule = animals.models.Schedule.objects.get(
            start_time=_utc(2023, 12, 25, 8)
        )

        self.assertEqual(test_schedule.start_time, _utc(2023, 12, 25, 8, 0))
        self.assertEqual(test_schedule.end_time, _utc(2023, 12, 25, 11, 0))
        self.assertEqual(test_schedule.user_id, 4)
        self.assertEqual(test_schedule.animal_id, self.test_animal.id)
        self.assertEqual(status_code, 200)

    def test_schedule_post_3(
        self,
    ):  # At the end of the working day + after booked interval
        test_client = self.logged_client()
        slot_payload = {
            "animal_id": self.test_animal.id,
            "selected_slot": "17:45",
            "selected_date": "2023-10-14",
            "duration_hours": 0,
            "duration_minutes": 15,
        }
        test_client.post("/schedule", data=slot_payload)
        response = test_client.post(
            "/schedule",
            data={**slot_payload, "confirm_schedule": "1"},
        )
        status_code = response.status_code
        test_schedule = animals.models.Schedule.objects.get(
            start_time=_utc(2023, 10, 14, 17, 45),
            end_time=_utc(2023, 10, 14, 18),
        )

        self.assertEqual(test_schedule.start_time, _utc(2023, 10, 14, 17, 45))
        self.assertEqual(test_schedule.end_time, _utc(2023, 10, 14, 18, 0))
        self.assertEqual(test_schedule.user_id, 4)
        self.assertEqual(test_schedule.animal_id, self.test_animal.id)
        self.assertEqual(status_code, 200)

    def test_schedule_post_fail(self):  # Conflict with another time
        test_client = self.logged_client()
        response = test_client.post(
            "/schedule",
            data={
                "animal_id": self.test_animal.id,
                "selected_slot": "10:00",
                "selected_date": "2023-10-14",
                "duration_hours": 8,
                "duration_minutes": 0,
            },
        )
        status_code = response.status_code
        is_test_schedule = animals.models.Schedule.objects.filter(
            start_time=_utc(2023, 10, 14, 10),
            end_time=_utc(2023, 10, 14, 18),
        ).exists()

        self.assertFalse(is_test_schedule)
        self.assertEqual(status_code, 200)

    def test_schedule_post_fail_2(self):  # Before opening
        test_client = self.logged_client()
        response = test_client.post(
            "/schedule",
            data={
                "animal_id": self.test_animal.id,
                "selected_slot": "04:00",
                "selected_date": "2023-10-25",
                "duration_hours": 1,
                "duration_minutes": 0,
            },
        )
        status_code = response.status_code
        is_test_schedule = animals.models.Schedule.objects.filter(
            start_time=_utc(2023, 10, 25, 4),
            end_time=_utc(2023, 10, 25, 5),
        ).exists()

        self.assertFalse(is_test_schedule)
        self.assertEqual(status_code, 200)

    def test_schedule_post_fail_3(self):  # After closure
        test_client = self.logged_client()
        response = test_client.post(
            "/schedule",
            data={
                "animal_id": self.test_animal.id,
                "selected_slot": "20:00",
                "selected_date": "2023-10-25",
                "duration_hours": 1,
                "duration_minutes": 0,
            },
        )
        status_code = response.status_code
        is_test_schedule = animals.models.Schedule.objects.filter(
            start_time=_utc(2023, 10, 25, 20),
            end_time=_utc(2023, 10, 25, 21),
        ).exists()

        self.assertFalse(is_test_schedule)
        self.assertEqual(status_code, 200)

    def test_schedule_post_fail_4(self):  # Test exception handling
        test_client = self.logged_client()
        response = test_client.post(
            "/schedule",
            data={
                "animal_id": self.test_animal.id,
                "selected_slot": "10:00",
                "selected_date": "2023-10-25",
                "duration_hours": "some bad data",
                "duration_minutes": "some bad data",
            },
        )
        status_code = response.status_code
        is_test_schedule = animals.models.Schedule.objects.filter(
            start_time=_utc(2023, 10, 25, 20),
            end_time=_utc(2023, 10, 25, 21),
        ).exists()

        self.assertFalse(is_test_schedule)
        self.assertEqual(status_code, 200)
