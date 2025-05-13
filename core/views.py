import os
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.services.import_sales import import_sales_from_static
from core.services.metrics import get_overall_metrics, get_daily_metrics
from core.utils.decorator import validate_request
from core.schemas import MetricsQueryParams
from core.utils.validate_date import validate_flow
from core.models import Sale
from django.conf import settings

class ImportSalesView(APIView):
    def get(self, request):
        static_dir = os.path.join(settings.BASE_DIR, 'core', 'static')
        total_rows = import_sales_from_static(static_dir)
        return Response({'imported_rows': total_rows}, status=status.HTTP_200_OK)

class GetOverallMetricsView(APIView):
    @validate_request(MetricsQueryParams)
    def get(self, request):
        params = MetricsQueryParams(**request.GET.dict())
        start_date, end_date, error = validate_flow(params.start, params.end)
        if error:
            return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)
        total_revenue_sgd, average_order_value_sgd = get_overall_metrics(start_date, end_date)
        return Response({
            'total_revenue_sgd': total_revenue_sgd,
            'average_order_value_sgd': average_order_value_sgd
        }, status=status.HTTP_200_OK)

class DailyMetricsView(APIView):
    @validate_request(MetricsQueryParams)
    def get(self, request):
        params = MetricsQueryParams(**request.GET.dict())
        start_date, end_date, error = validate_flow(params.start, params.end)
        if error:
            return Response({'message': error}, status=status.HTTP_400_BAD_REQUEST)
        daily_metrics = get_daily_metrics(start_date, end_date)
        return Response(daily_metrics, status=status.HTTP_200_OK)

class HealthCheckView(APIView):
    def get(self, request):
        try:
            Sale.objects.count()
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'status': 'ok',  "database": "reachable" }, status=status.HTTP_200_OK)