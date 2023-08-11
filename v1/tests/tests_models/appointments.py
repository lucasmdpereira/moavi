from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from v1.models.appointments import Appointments
from v1.models.consumptions import Consumptions
from datetime import datetime
from django.core.exceptions import ValidationError


class AppointmentsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@example.com', password='password')
        self.consumption = Consumptions.objects.create(file_name='test.csv', appointments_entries=5, imported_by=self.user)

    def test_appointment_creation(self):
        appointment = Appointments.objects.create(registration_id=123, scheduling=datetime.now(), created_by=self.consumption)
        self.assertIsInstance(appointment, Appointments)

    def test_str_method(self):
        appointment = Appointments.objects.create(registration_id=123, scheduling=datetime.now(), created_by=self.consumption)
        self.assertEqual(str(appointment), str(appointment.pk))

    def test_registration_id_integer_validation(self):
        with self.assertRaises(ValidationError):
            Appointments.objects.create(registration_id="invalid", scheduling=datetime.now(), created_by=self.consumption)

    def test_registration_id_positive_validation(self):
        with self.assertRaises(ValidationError):
            appointment = Appointments.objects.create(registration_id=-123, scheduling=datetime.now(), created_by=self.consumption)
            appointment.full_clean()

    def test_foreign_key_relation_with_consumptions(self):
        appointment = Appointments.objects.create(registration_id=123, scheduling=datetime.now(), created_by=self.consumption)
        self.assertEqual(appointment.created_by, self.consumption)
