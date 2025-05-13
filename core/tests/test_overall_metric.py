from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime, timedelta
from core.models import Sale


class GetOverallMetricsViewTest(APITestCase):
    def setUp(self):
        today = datetime.today().date()
        seed_data = [
            Sale(date=today - timedelta(days=i), order_id=str(i), amount_sgd=100 + i, product_id=f'P{i}')
            for i in range(5)
        ]
        Sale.objects.bulk_create(seed_data)

        self.client = APIClient()

    def test_metrics_valid(self):
        url = reverse('metrics-revenue')
        today = datetime.today().date()
        params = {
            'start': (today - timedelta(days=4)).strftime('%Y-%m-%d'),
            'end': today.strftime('%Y-%m-%d'),
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_revenue_sgd', response.data)
        self.assertIn('average_order_value_sgd', response.data)
        self.assertEqual(response.data['total_revenue_sgd'], 510)
        self.assertEqual(response.data['average_order_value_sgd'], 102)

    def test_metrics_invalid_date(self):
        url = reverse('metrics-revenue')
        params = {'start': 'invalid', 'end': 'invalid'}
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)

    def test_metrics_missing_params(self):
        url = reverse('metrics-revenue')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data) 
    
    def tearDown(self):
        Sale.objects.all().delete()