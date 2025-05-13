from datetime import datetime
from django.conf import settings
from core.models import Sale
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate

def get_overall_metrics(start_date: datetime, end_date: datetime):
    total_revenue_sgd = Sale.objects.filter(date__range=(start_date, end_date)).aggregate(total_revenue=Sum('amount_sgd'))['total_revenue'] or 0
    total_orders = Sale.objects.filter(date__range=(start_date, end_date)).count()
    average_order_value_sgd = total_revenue_sgd / total_orders if total_orders > 0 else 0
    return total_revenue_sgd, average_order_value_sgd

def get_daily_metrics(start_date: datetime, end_date: datetime) -> list[dict]:
    daily_metrics = Sale.objects.filter(date__range=(start_date, end_date)).annotate(
        date_only=TruncDate('date')
    ).values('date_only').annotate(
        revenue_sgd=Sum('amount_sgd')
    ).order_by('date_only')
    
    return [
        {
            'date': metric['date_only'],
            'revenue_sgd': metric['revenue_sgd'],
        }
        for metric in daily_metrics
    ]
