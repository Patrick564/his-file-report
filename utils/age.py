from datetime import datetime
from zoneinfo import ZoneInfo


def get_age(birth_date: str):
    start = datetime.strptime(birth_date, "%Y-%m-%d %H:%M:%S").date()
    today = datetime.now(tz=ZoneInfo("America/Lima")).date()

    difference = today - start

    years = difference.days // 365
    months = (difference.days % 365) // 30
    days = (difference.days % 365) % 30

    return f"{start.day}     {start.month}     {start.year}", {
        "years": str(abs(years)),
        "months": str(abs(months)),
        "days": str(abs(days)),
    }
