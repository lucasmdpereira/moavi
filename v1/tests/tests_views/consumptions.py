from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from v1.models import Consumptions


class ConsumptionsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.consumption = Consumptions.objects.create(file_name='example.csv', appointments_entries=2, imported_by=cls.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('consumptions'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('consumptions'))
        self.assertTemplateUsed(response, 'consumptions.html')