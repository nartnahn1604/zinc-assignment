from datetime import datetime

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    if start_date > end_date:
        return False
    return True 

def validate_flow(start_date: str, end_date: str) -> tuple[datetime | None, datetime | None, str | None]:
    if not validate_date(start_date) or not validate_date(end_date):
        return None, None, "Invalid date format"
    if not validate_date_range(start_date, end_date):
        return None, None, "Start date must be before end date"
    return start_date, end_date, None