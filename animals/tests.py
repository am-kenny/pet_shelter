from django.contrib.auth.models import User
from django.test import TestCase, Client
import unittest
import datetime

from django.urls import reverse

import animals.models
from animals.utils import available_booking_times


# Schedule testing
class TestScheduleSortedPeriods(unittest.TestCase):
    def test_schedule_1(self):
        expected = ['08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '12:00', '12:15', '12:30', '16:00',
                    '16:15', '16:30']
        booked = [(datetime.datetime(2023, 9, 12, 11, 0),
                   datetime.datetime(2023, 9, 12, 12, 0)),
                  (datetime.datetime(2023, 9, 12, 14, 0),
                   datetime.datetime(2023, 9, 12, 16, 0))]
        hours = 1
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_2(self):
        expected = ['08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '14:00', '14:15', '14:30', '14:45',
                    '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30']
        booked = [(datetime.datetime(2023, 9, 12, 11, 0),
                   datetime.datetime(2023, 9, 12, 12, 0)),
                  (datetime.datetime(2023, 9, 12, 12, 0),
                   datetime.datetime(2023, 9, 12, 14, 0))]
        hours = 1
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_3(self):
        expected = ['08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '14:00', '14:15', '14:30', '14:45',
                    '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30']
        booked = [(datetime.datetime(2024, 1, 15, 11, 0),
                   datetime.datetime(2024, 1, 15, 12, 0)),
                  (datetime.datetime(2024, 1, 15, 12, 0),
                   datetime.datetime(2024, 1, 15, 14, 0))]
        hours = 1
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_4(self):
        expected = ['09:00', '09:15', '09:30', '09:45', '10:00', '10:15', '10:30', '14:00', '14:15', '14:30', '14:45',
                    '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30']
        booked = [(datetime.datetime(2023, 9, 12, 8, 0),
                   datetime.datetime(2023, 9, 12, 9, 0)),
                  (datetime.datetime(2023, 9, 12, 12, 0),
                   datetime.datetime(2023, 9, 12, 14, 0))]
        hours = 1
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_5(self):
        expected = []
        booked = [(datetime.datetime(2023, 9, 12, 8, 0),
                   datetime.datetime(2023, 9, 12, 9, 0)),
                  (datetime.datetime(2023, 9, 12, 10, 0),
                   datetime.datetime(2023, 9, 12, 14, 0)),
                  (datetime.datetime(2023, 9, 12, 15, 0),
                   datetime.datetime(2023, 9, 12, 17, 0))]
        hours = 1
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_6(self):
        expected = ['09:00', '09:15', '09:30', '09:45', '14:30', '14:45', '17:00', '17:15', '17:30', '17:45']
        booked = [(datetime.datetime(2023, 9, 12, 8, 0),
                   datetime.datetime(2023, 9, 12, 9, 0)),
                  (datetime.datetime(2023, 9, 12, 10, 0),
                   datetime.datetime(2023, 9, 12, 14, 30)),
                  (datetime.datetime(2023, 9, 12, 15, 0),
                   datetime.datetime(2023, 9, 12, 17, 0))]
        hours = 0
        minutes = 15
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)


class TestScheduleUnsortedPeriods(unittest.TestCase):
    def test_schedule_1(self):
        expected = ['15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30']
        booked = [(datetime.datetime(2023, 9, 12, 13, 0),
                   datetime.datetime(2023, 9, 12, 14, 0)),
                  (datetime.datetime(2023, 9, 12, 11, 0),
                   datetime.datetime(2023, 9, 12, 12, 0)),
                  (datetime.datetime(2023, 9, 12, 14, 0),
                   datetime.datetime(2023, 9, 12, 15, 0)),
                  (datetime.datetime(2023, 9, 12, 9, 0),
                   datetime.datetime(2023, 9, 12, 10, 0))]
        hours = 1
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_2(self):
        expected = ['14:00', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00', '16:15', '16:30']
        booked = [(datetime.datetime(2023, 9, 12, 13, 0),
                   datetime.datetime(2023, 9, 12, 14, 0)),
                  (datetime.datetime(2023, 9, 12, 11, 0),
                   datetime.datetime(2023, 9, 12, 12, 0)),
                  (datetime.datetime(2023, 9, 12, 9, 0),
                   datetime.datetime(2023, 9, 12, 10, 0))]
        hours = 1
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_3(self):
        expected = ['15:00', '15:15']
        booked = [(datetime.datetime(2023, 12, 18, 13, 0),
                   datetime.datetime(2023, 12, 18, 14, 0)),
                  (datetime.datetime(2023, 12, 18, 11, 0),
                   datetime.datetime(2023, 12, 18, 12, 0)),
                  (datetime.datetime(2023, 12, 18, 14, 0),
                   datetime.datetime(2023, 12, 18, 15, 0)),
                  (datetime.datetime(2023, 12, 18, 9, 0),
                   datetime.datetime(2023, 12, 18, 10, 0))]
        hours = 2
        minutes = 45
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)


class TestScheduleEmpty(unittest.TestCase):
    def test_schedule_1(self):
        expected = ['08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45', '10:00', '10:15', '10:30',
                    '10:45', '11:00', '11:15', '11:30', '11:45', '12:00', '12:15', '12:30', '12:45', '13:00', '13:15',
                    '13:30', '13:45', '14:00', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00',
                    '16:15', '16:30']
        booked = []
        hours = 1
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_2(self):
        expected = ['08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45', '10:00', '10:15', '10:30',
                    '10:45', '11:00', '11:15', '11:30', '11:45', '12:00', '12:15', '12:30', '12:45', '13:00', '13:15',
                    '13:30', '13:45', '14:00', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00',
                    '16:15', '16:30', '16:45', '17:00', '17:15', '17:30']
        booked = []
        hours = 0
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_4(self):
        expected = ['08:00', '08:15', '08:30']
        booked = []
        hours = 9
        minutes = 30
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_5(self):
        expected = ['08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45', '10:00', '10:15', '10:30',
                    '10:45', '11:00', '11:15', '11:30', '11:45', '12:00', '12:15', '12:30', '12:45', '13:00', '13:15',
                    '13:30', '13:45', '14:00', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45', '16:00',
                    '16:15', '16:30', '16:45', '17:00', '17:15', '17:30', '17:45']
        booked = []
        hours = 0
        minutes = 15
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_one_available(self):
        expected = ['08:00']
        booked = []
        hours = 10
        minutes = 0
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)

    def test_schedule_no_available(self):
        expected = []
        booked = []
        hours = 10
        minutes = 15
        result = available_booking_times(booked, hours, minutes)
        self.assertEqual(result, expected)


# Endpoints testing
class TestAnimals(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.test_animal = animals.models.Animal.objects.filter(id=3).first()

    def test_animals_page(self):
        test_client = Client()
        response = test_client.get('/animals')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_animal_page(self):
        test_client = Client()
        response = test_client.get(reverse('animal', args=[self.test_animal.id]))
        status_code = response.status_code
        has_animal_name = self.test_animal.name in response.content.decode('utf-8')
        self.assertEqual(status_code, 200)
        self.assertTrue(has_animal_name)

    def test_animal_page_fail(self):  # Unexisting animal
        test_client = Client()
        response = test_client.get(reverse('animal', args=[777]))
        status_code = response.status_code
        self.assertEqual(status_code, 404)


class TestAnimalSchedule(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.test_animal = animals.models.Animal.objects.filter(id=3).first()

    @staticmethod
    def logged_client():
        test_client = Client()
        test_client.login(username='guest', password='vfRarYj37Jfp@V3')
        return test_client

    def test_schedule_get_1(self):
        test_client = self.logged_client()
        response = test_client.get('/schedule')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_schedule_get_2(self):
        test_client = self.logged_client()
        response = test_client.get('/schedule', data={'animal_id': self.test_animal.id,
                                                      "date": "2023-10-14",
                                                      "duration_hours": 1,
                                                      "duration_minutes": 0})
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_schedule_get_3(self):
        test_client = Client()
        response = test_client.get('/schedule')
        status_code = response.status_code
        self.assertEqual(status_code, 302)

    def test_schedule_get_4(self):  # Test exception handling
        test_client = self.logged_client()
        response = test_client.get('/schedule', data={'animal_id': self.test_animal.id,
                                                      "date": "2023-10-14",
                                                      "duration_hours": "some bad data",
                                                      "duration_minutes": "some bad data"})
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_schedule_get_fail(self):  # Unexisting animal
        test_client = self.logged_client()
        response = test_client.get('/schedule', data={'animal_id': 777,
                                                      "date": "2023-10-13",
                                                      "duration_hours": 1,
                                                      "duration_minutes": 0})
        status_code = response.status_code
        self.assertEqual(status_code, 404)

    def test_schedule_post(self):
        test_client = self.logged_client()
        response = test_client.post('/schedule', data={'animal_id': self.test_animal.id,
                                                       'selected_slot': '10:00',
                                                       'selected_date': '2023-12-14',
                                                       'duration_hours': 1,
                                                       'duration_minutes': 0})
        status_code = response.status_code
        test_schedule = animals.models.Schedule.objects.get(start_time=datetime.datetime(2023, 12, 14, 10))

        self.assertEqual(test_schedule.start_time, datetime.datetime(2023, 12, 14, 10, 0))
        self.assertEqual(test_schedule.end_time, datetime.datetime(2023, 12, 14, 11, 0))
        self.assertEqual(test_schedule.user_id, 4)
        self.assertEqual(test_schedule.animal_id, self.test_animal.id)
        self.assertEqual(status_code, 200)

    def test_schedule_post_2(self):  # At the start of the working day
        test_client = self.logged_client()
        response = test_client.post('/schedule', data={'animal_id': self.test_animal.id,
                                                       'selected_slot': '08:00',
                                                       'selected_date': '2023-12-25',
                                                       'duration_hours': 3,
                                                       'duration_minutes': 0})
        status_code = response.status_code
        test_schedule = animals.models.Schedule.objects.get(start_time=datetime.datetime(2023, 12, 25, 8))

        self.assertEqual(test_schedule.start_time, datetime.datetime(2023, 12, 25, 8, 0))
        self.assertEqual(test_schedule.end_time, datetime.datetime(2023, 12, 25, 11, 0))
        self.assertEqual(test_schedule.user_id, 4)
        self.assertEqual(test_schedule.animal_id, self.test_animal.id)
        self.assertEqual(status_code, 200)

    def test_schedule_post_3(self):  # At the end of the working day + after booked interval
        test_client = self.logged_client()
        response = test_client.post('/schedule', data={'animal_id': self.test_animal.id,
                                                       'selected_slot': '17:45',
                                                       'selected_date': '2023-10-14',
                                                       'duration_hours': 0,
                                                       'duration_minutes': 15})
        status_code = response.status_code
        test_schedule = animals.models.Schedule.objects.get(start_time=datetime.datetime(2023, 10, 14, 17, 45),
                                                            end_time=datetime.datetime(2023, 10, 14, 18))

        self.assertEqual(test_schedule.start_time, datetime.datetime(2023, 10, 14, 17, 45))
        self.assertEqual(test_schedule.end_time, datetime.datetime(2023, 10, 14, 18, 0))
        self.assertEqual(test_schedule.user_id, 4)
        self.assertEqual(test_schedule.animal_id, self.test_animal.id)
        self.assertEqual(status_code, 200)

    def test_schedule_post_fail(self):  # Conflict with another time
        test_client = self.logged_client()
        response = test_client.post('/schedule', data={'animal_id': self.test_animal.id,
                                                       'selected_slot': '10:00',
                                                       'selected_date': '2023-10-14',
                                                       'duration_hours': 8,
                                                       'duration_minutes': 0})
        status_code = response.status_code
        is_test_schedule = animals.models.Schedule.objects.filter(start_time=datetime.datetime(2023, 10, 14, 10),
                                                                  end_time=datetime.datetime(2023, 10, 14, 18)).exists()

        self.assertFalse(is_test_schedule)
        self.assertEqual(status_code, 200)

    def test_schedule_post_fail_2(self):  # Before opening
        test_client = self.logged_client()
        response = test_client.post('/schedule', data={'animal_id': self.test_animal.id,
                                                       'selected_slot': '04:00',
                                                       'selected_date': '2023-10-25',
                                                       'duration_hours': 1,
                                                       'duration_minutes': 0})
        status_code = response.status_code
        is_test_schedule = animals.models.Schedule.objects.filter(start_time=datetime.datetime(2023, 10, 25, 4),
                                                                  end_time=datetime.datetime(2023, 10, 25, 5)).exists()

        self.assertFalse(is_test_schedule)
        self.assertEqual(status_code, 200)

    def test_schedule_post_fail_3(self):  # After closure
        test_client = self.logged_client()
        response = test_client.post('/schedule', data={'animal_id': self.test_animal.id,
                                                       'selected_slot': '20:00',
                                                       'selected_date': '2023-10-25',
                                                       'duration_hours': 1,
                                                       'duration_minutes': 0})
        status_code = response.status_code
        is_test_schedule = animals.models.Schedule.objects.filter(start_time=datetime.datetime(2023, 10, 25, 20),
                                                                  end_time=datetime.datetime(2023, 10, 25, 21)).exists()

        self.assertFalse(is_test_schedule)
        self.assertEqual(status_code, 200)

    def test_schedule_post_fail_4(self):  # Test exception handling
        test_client = self.logged_client()
        response = test_client.post('/schedule', data={'animal_id': self.test_animal.id,
                                                       'selected_slot': '10:00',
                                                       'selected_date': '2023-10-25',
                                                       'duration_hours': "some bad data",
                                                       'duration_minutes': "some bad data"})
        status_code = response.status_code
        is_test_schedule = animals.models.Schedule.objects.filter(start_time=datetime.datetime(2023, 10, 25, 20),
                                                                  end_time=datetime.datetime(2023, 10, 25, 21)).exists()

        self.assertFalse(is_test_schedule)
        self.assertEqual(status_code, 200)
