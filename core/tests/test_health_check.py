from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

class HealthCheckViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health_check(self):
        url = reverse('health-check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'ok')