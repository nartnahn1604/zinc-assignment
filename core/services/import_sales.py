import os
import pandas as pd
from datetime import datetime
from django.conf import settings
from core.models import Sale, ImportedFile

def parse_sale_row(row):
    try:
        sale_date = row.get('Sale Date', '').strip()
        order_id = str(row.get('Sale ID', '')).strip()
        amount_sgd = row.get('Subtotal (excluding tax)', None)
        product_id = str(row.get('Item name', '')).strip()
        date_obj = datetime.strptime(sale_date, '%m/%d/%Y')
        sale_date = date_obj.strftime('%Y-%m-%d')
        return dict(date=sale_date, order_id=order_id, amount_sgd=amount_sgd, product_id=product_id)
    except Exception:
        return None

def import_sales_from_static(path=None):
    total_rows = 0
    if not path:
        path = os.path.join(settings.BASE_DIR, 'core', 'static')
    if not os.path.exists(path):
        return 0
    
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    for filename in csv_files:
        imported_file = ImportedFile.objects.filter(filename=filename, status='success').first()
        if imported_file:
            total_rows += imported_file.num_rows
            continue
        file_path = os.path.join(path, filename)
        file_imported = 0
        status_str = 'success'
        sales_to_create = []
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()
            for _, row in df.iterrows():
                sale_data = parse_sale_row(row)
                if sale_data:
                    sales_to_create.append(Sale(**sale_data))
                    file_imported += 1
        except Exception:
            status_str = 'error'
        imported_file_obj = ImportedFile.objects.create(
            filename=filename,
            num_rows=file_imported,
            status=status_str,
            error_message=''
        )
        # Bulk create and link to ImportedFile
        for sale in sales_to_create:
            sale.imported_file = imported_file_obj
        Sale.objects.bulk_create(sales_to_create)
        total_rows += file_imported
    return total_rows 