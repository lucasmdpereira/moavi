from django.test import TestCase
from django.contrib.auth.models import User
from v1.models.consumptions import Consumptions
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


class ConsumptionsModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')

        self.consumption = Consumptions.objects.create(
            file_name="test_file.csv",
            appointments_entries=5,
            imported_by=self.user
        )

    def test_str_method(self):
        self.assertEqual(str(self.consumption), str(self.consumption.pk))

    def test_file_name_label(self):
        field_label = self.consumption._meta.get_field('file_name').verbose_name
        self.assertEqual(field_label, 'file name')

    def test_appointments_entries_label(self):
        field_label = self.consumption._meta.get_field('appointments_entries').verbose_name
        self.assertEqual(field_label, 'appointments entries')

    def test_imported_by_label(self):
        field_label = self.consumption._meta.get_field('imported_by').verbose_name
        self.assertEqual(field_label, 'imported by')

    def test_imported_by_foreign_key(self):
        field_foreign_key = self.consumption._meta.get_field('imported_by').remote_field.model
        self.assertEqual(field_foreign_key, User)

    def test_created_at_auto_now_add(self):
        self.consumption.refresh_from_db()
        self.assertAlmostEqual(self.consumption.created_at.replace(tzinfo=None), datetime.now(), delta=timedelta(seconds=1))

    def test_file_name_max_length(self):
        long_file_name = 'a' * 256
        with self.assertRaises(ValidationError):
            consumption = Consumptions(file_name=long_file_name, appointments_entries=5, imported_by=self.user)
            consumption.full_clean()

    def test_file_name_not_empty(self):
        with self.assertRaises(ValidationError):
            consumption = Consumptions(file_name='', appointments_entries=5, imported_by=self.user)
            consumption.full_clean()

    def test_appointments_entries_not_negative(self):
        with self.assertRaises(ValidationError):
            consumption = Consumptions(file_name='test_file.csv', appointments_entries=-5, imported_by=self.user)
            consumption.full_clean()

    def test_imported_by_is_user_instance(self):
        with self.assertRaises(ValueError):
            consumption = Consumptions(file_name='test_file.csv', appointments_entries=5, imported_by='invalid_user')
            consumption.full_clean()