from datetime import date

from curio import loans


def test_overdue_filters_on_end_date(monkeypatch):
    rows = [{"accession": "a", "ends": "2026-01-01"}, {"accession": "b", "ends": "2027-01-01"}, {"accession": "c", "ends": None}]
    monkeypatch.setattr(loans, "on_loan", lambda today=None: rows)
    assert [row["accession"] for row in loans.overdue(date(2026, 6, 1))] == ["a"]
