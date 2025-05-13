from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime, timedelta
from core.models import Sale

class DailyMetricsViewTest(APITestCase):
    def setUp(self):
        today = datetime.today().date()
        seed_data = [
            Sale(date=today - timedelta(days=i), order_id=str(i), amount_sgd=100 + i, product_id=f'P{i}')
            for i in range(5)
        ]
        Sale.objects.bulk_create(seed_data)
        self.client = APIClient()

    def test_daily_metrics_valid(self):
        url = reverse('metrics-daily')
        today = datetime.today().date()
        params = {
            'start': (today - timedelta(days=4)).strftime('%Y-%m-%d'),
            'end': today.strftime('%Y-%m-%d'),
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 5)
        for entry in response.data:
            self.assertIn('date', entry)
            self.assertIn('revenue_sgd', entry)

    def test_daily_metrics_invalid_date(self):
        url = reverse('metrics-daily')
        params = {'start': 'invalid', 'end': 'invalid'}
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)

    def test_daily_metrics_missing_params(self):
        url = reverse('metrics-daily')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)

    def tearDown(self):
        Sale.objects.all().delete()