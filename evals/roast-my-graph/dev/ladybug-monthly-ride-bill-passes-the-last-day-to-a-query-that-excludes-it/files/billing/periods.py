"""Billing periods. A period is the first and the last day of a calendar month."""
import calendar
from datetime import date


def month_period(year, month):
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    return first_day, last_day


def previous_month(today):
    if today.month == 1:
        return month_period(today.year - 1, 12)
    return month_period(today.year, today.month - 1)
