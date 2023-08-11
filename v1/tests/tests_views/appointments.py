from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from v1.models import Appointments, Consumptions


class AppointmentsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpassword')
        consumption = Consumptions.objects.create(file_name='example.csv', appointments_entries=2, imported_by=user)

        Appointments.objects.create(registration_id=1001, scheduling='2023-08-10 10:00', created_by=consumption)
        Appointments.objects.create(registration_id=1002, scheduling='2023-08-11 14:30', created_by=consumption)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('appointments'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('appointments'))
        self.assertTemplateUsed(response, 'appointments.html')

    def test_search_by_date(self):
        response = self.client.get(reverse('appointments'), {'search': '2023-08-10'})
        self.assertEqual(response.status_code, 200)

    def test_search_by_file_name(self):
        response = self.client.get(reverse('appointments'), {'search': 'example.csv'})
        self.assertEqual(response.status_code, 200)

    def test_search_by_registration_id(self):
        response = self.client.get(reverse('appointments'), {'search': '1002'})
        self.assertEqual(response.status_code, 200)

    def test_invalid_date_search(self):
        response = self.client.get(reverse('appointments'), {'search': 'invalid-date'})
        self.assertEqual(response.status_code, 200)
