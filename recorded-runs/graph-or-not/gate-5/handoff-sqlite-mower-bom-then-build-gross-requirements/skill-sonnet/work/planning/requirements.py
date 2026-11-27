"""Gross requirements: bought-in parts needed to make a quantity of an item."""
from . import sqlfile


def gross_requirements(conn, item_id, qty):
    """Return {item_id: quantity} for every bought-in part (make_buy = 'B') needed for qty of item_id.

    Follows the BOM to any depth. Scrap of 4% is added on every BOM line and compounds down the
    levels, so a part three levels down carries 1.04 ** 3. Quantities are rounded to 3 decimals.
    """
    rows = sqlfile.fetch_all(conn, "gross_requirements.sql", item_id=item_id, qty=qty)
    return {row[0]: round(row[1], 3) for row in rows}
