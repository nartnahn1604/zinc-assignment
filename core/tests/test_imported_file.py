import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from core.models import Sale


class ImportSalesViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_import_sales_and_log(self):
        url = reverse('import-sales')
        with self.assertLogs(level='INFO') as cm:
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        imported_rows = response.data.get('imported_rows')
        self.assertIsNotNone(imported_rows)
        self.assertEqual(Sale.objects.count(), imported_rows)

        log_line = next((line for line in cm.output if 'imported_rows' in line), None)
        self.assertIsNotNone(log_line, "No 'imported_rows' log found")
        try:
            json_part = log_line.split(":", 2)[-1].strip().replace("'", '"')
            log_data = json.loads(json_part)
            self.assertEqual(log_data['imported_rows'], imported_rows)
        except Exception as e:
            self.fail(f"Could not parse log JSON: {e}")

    def tearDown(self):
        Sale.objects.all().delete()