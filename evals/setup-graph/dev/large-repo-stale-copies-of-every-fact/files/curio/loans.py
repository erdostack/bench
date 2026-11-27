from datetime import date

from . import graph


def on_loan(today: date | None = None) -> list[dict]:
    return graph.read(graph.saved("on_loan_now"), today=(today or date.today()).isoformat())


def overdue(today: date | None = None) -> list[dict]:
    day = (today or date.today()).isoformat()
    return [row for row in on_loan(today) if row["ends"] and row["ends"] < day]
