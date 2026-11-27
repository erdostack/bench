"""Gross requirements for bought-in parts."""
from . import sqlfile


def gross_requirements(conn, item_id, qty):
    """Return {item_id: quantity} for every bought-in part (make_buy = 'B') needed to make qty of item_id.

    Uses sql/gross_requirements.sql, so the 4% per-line compounding scrap rule applies. Quantities are
    rounded to 3 decimals.
    """
    rows = sqlfile.fetch_all(conn, "gross_requirements.sql", item_id=item_id, qty=qty)
    return {row[0]: round(row[4], 3) for row in rows}
