"""Gross requirements: explode a made item down its BOM to the bought-in parts it needs."""
from collections import defaultdict

from . import sqlfile


def gross_requirements(conn, item_id, qty):
    """Return {item_id: quantity} for every bought-in part (make_buy = 'B') needed to make qty of item_id.

    Walks the BOM all the way down, multiplying qty_per at each level. Bought-in parts are leaves: their
    own BOM lines (if any) are not exploded. Quantities are rounded to 3 decimals.
    """
    top = sqlfile.fetch_all(conn, "item_make_buy.sql", item_id=item_id)
    if not top:
        raise ValueError(f"no item with id {item_id}")
    if top[0][0] == "B":
        return {item_id: round(float(qty), 3)}

    totals = defaultdict(float)
    # Each entry: (made item id, quantity of it needed, ids on the path from the top, for cycle detection)
    stack = [(item_id, float(qty), (item_id,))]
    while stack:
        parent, need, path = stack.pop()
        for component_id, _part_no, _description, qty_per, make_buy in sqlfile.fetch_all(
            conn, "bom_first_level.sql", item_id=parent
        ):
            child_need = need * qty_per
            if make_buy == "B":
                totals[component_id] += child_need
            else:
                if component_id in path:
                    raise ValueError(f"BOM cycle through item {component_id}")
                stack.append((component_id, child_need, path + (component_id,)))

    return {item: round(total, 3) for item, total in totals.items()}
