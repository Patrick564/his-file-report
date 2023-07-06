from datetime import datetime
from typing import NamedTuple
from zoneinfo import ZoneInfo


class CurrentAge(NamedTuple):
    years: int
    months: int
    days: int
    format: str


def full_age(birthday: str) -> CurrentAge:
    start = datetime.strptime(birthday, "%Y-%m-%d %H:%M:%S").date()
    today = datetime.now(tz=ZoneInfo("America/Lima")).date()

    difference = today - start

    years = difference.days // 365
    months = (difference.days % 365) // 30
    days = (difference.days % 365) % 30

    return CurrentAge(
        years=abs(years),
        months=abs(months),
        days=abs(days),
        format=f"{start.day}     {start.month}     {start.year}",
    )


# def format_age(birthday: str):
#     start = datetime.strptime(birthday, "%Y-%m-%d %H:%M:%S").date()

#     return f"{start.day}     {start.month}     {start.year}"


# def full_age(birthday: str):
#     start = datetime.strptime(birthday, "%Y-%m-%d %H:%M:%S").date()
#     today = datetime.now(tz=ZoneInfo("America/Lima")).date()

#     difference = today - start

#     years = difference.days // 365
#     months = (difference.days % 365) // 30
#     days = (difference.days % 365) % 30

#     return {
#         "years": abs(years),
#         "months": abs(months),
#         "days": abs(days),
#     }
