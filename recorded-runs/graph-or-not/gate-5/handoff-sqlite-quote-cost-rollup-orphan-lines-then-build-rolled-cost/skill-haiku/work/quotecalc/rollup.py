"""Rolled-up unit cost of an item, from its bill of materials."""

MAX_DEPTH = 7  # BOMs go up to 7 levels; the walk stops here

# Every component reached from the item within MAX_DEPTH levels, one row per path. Only made items are
# expanded, so a bought item's own BOM (if any) is never followed.
_WALK = """
WITH RECURSIVE walk (component_id, mult, depth) AS (
    SELECT b.component_id, b.qty, 1
    FROM bom_line b
    WHERE b.parent_id = :item_id
    UNION ALL
    SELECT b.component_id, w.mult * b.qty, w.depth + 1
    FROM walk w
    JOIN item p ON p.id = w.component_id AND p.kind = 'made'
    JOIN bom_line b ON b.parent_id = w.component_id
    WHERE w.depth < :max_depth
)
SELECT w.component_id, w.mult, i.kind, i.std_cost, i.labour_cost
FROM walk w LEFT JOIN item i ON i.id = w.component_id
"""


def rolled_cost(conn, item_id):
    """Unit cost of item_id: a bought item's std_cost, or a made item's labour_cost plus qty times the rolled
    cost of each component, summed over the whole BOM. Returns None when any item under it is missing from
    the item table or has no cost, so a partial total is never returned."""
    root = conn.execute("SELECT kind, std_cost, labour_cost FROM item WHERE id = ?", (item_id,)).fetchone()
    if root is None:
        return None
    kind, std_cost, labour_cost = root
    if kind == "bought":
        return std_cost
    if labour_cost is None:
        return None
    total = labour_cost
    for _component_id, mult, comp_kind, comp_std, comp_labour in conn.execute(
            _WALK, {"item_id": item_id, "max_depth": MAX_DEPTH}):
        if comp_kind is None:
            return None  # a component is missing from the item table
        own = comp_std if comp_kind == "bought" else comp_labour
        if own is None:
            return None
        total += mult * own
    return total
