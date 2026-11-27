"""Gross requirements: the bought-in parts needed to make a quantity of an item."""
from . import sqlfile

MAX_DEPTH = 11  # deepest BOM the walk follows (planning lead and product owner set this)
LINE_FACTOR = 1.04  # 4% scrap on every BOM line


def gross_requirements(conn, item_id, qty):
    """Return {bought-in item id: quantity} needed to make qty of item_id, to 3 decimals."""
    rows = sqlfile.fetch_all(
        conn,
        "gross_requirements.sql",
        item_id=item_id,
        max_depth=MAX_DEPTH,
        line_factor=LINE_FACTOR,
    )
    return {component_id: round(per_unit * qty, 3) for component_id, per_unit in rows}
