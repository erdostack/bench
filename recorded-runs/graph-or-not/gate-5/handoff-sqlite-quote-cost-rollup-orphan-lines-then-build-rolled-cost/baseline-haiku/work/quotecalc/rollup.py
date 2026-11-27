"""Rolled-up unit cost: what an item costs once its whole bill of materials is priced."""


def rolled_cost(conn, item_id):
    """Rolled-up unit cost of item_id.

    A bought item costs its std_cost. A made item costs its labour_cost plus qty times the rolled cost of
    each of its components, at every level of the BOM. Bought items are priced at std_cost and their own
    BOM lines are not walked. Raises ValueError if an item is missing, a cost it needs is missing, or the
    BOM loops, rather than quoting a wrong cost.
    """
    return _rolled(conn, item_id, ())


def _rolled(conn, item_id, path):
    if item_id in path:
        raise ValueError(f"BOM cycle through item {item_id}")
    row = conn.execute("SELECT kind, std_cost, labour_cost FROM item WHERE id = ?", (item_id,)).fetchone()
    if row is None:
        raise ValueError(f"no item with id {item_id}")
    kind, std_cost, labour_cost = row
    if kind == "bought":
        if std_cost is None:
            raise ValueError(f"bought item {item_id} has no std_cost")
        return std_cost
    if labour_cost is None:
        raise ValueError(f"made item {item_id} has no labour_cost")
    total = labour_cost
    for component_id, qty in conn.execute(
        "SELECT component_id, qty FROM bom_line WHERE parent_id = ?", (item_id,)
    ).fetchall():
        total += qty * _rolled(conn, component_id, path + (item_id,))
    return total
