from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from v1.models import Appointments, Consumptions
from datetime import datetime
import pytz


class SchedulesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        local_tz = pytz.timezone('UTC')

        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.consumption = Consumptions.objects.create(file_name='example.csv', appointments_entries=4, imported_by=cls.user)

        cls.appointment1 = Appointments.objects.create(registration_id=1001, scheduling=local_tz.localize(datetime(2023, 8, 10, 10, 0)), created_by=cls.consumption)
        cls.appointment2 = Appointments.objects.create(registration_id=1002, scheduling=local_tz.localize(datetime(2023, 8, 10, 10, 30)), created_by=cls.consumption)
        cls.appointment3 = Appointments.objects.create(registration_id=1003, scheduling=local_tz.localize(datetime(2023, 8, 10, 11, 0)), created_by=cls.consumption)
        cls.appointment4 = Appointments.objects.create(registration_id=1004, scheduling=local_tz.localize(datetime(2023, 8, 11, 12, 0)), created_by=cls.consumption)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('schedules'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('schedules'))
        self.assertTemplateUsed(response, 'schedules.html')

    def test_schedules_on_selected_date(self):
        response = self.client.get(reverse('schedules'), {'date': '2023-08-10'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['labels']), 144)
        self.assertEqual(len(response.context['data']), 144)
        self.assertEqual(response.context['date'].date(), datetime(2023, 8, 10).date())

    def test_schedules_on_non_existent_date(self):
        response = self.client.get(reverse('schedules'), {'date': '2023-08-09'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['labels']), 144)
        self.assertEqual(len(response.context['data']), 144)
        self.assertEqual(response.context['date'].date(), datetime(2023, 8, 9).date())

