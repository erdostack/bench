"""Rolled-up unit cost of an item through all levels of its BOM."""

# Deepest BOM is 7 levels (docs/graph/DECISION.md). The schema does not stop a cycle, so the walk is capped.
MAX_DEPTH = 12

_ROLLUP_SQL = """
WITH RECURSIVE walk (item_id, mult, depth) AS (
    SELECT :item_id, 1.0, 0
    UNION ALL
    SELECT b.component_id, w.mult * b.qty, w.depth + 1
    FROM walk w
    JOIN item p ON p.id = w.item_id AND p.kind = 'made'
    JOIN bom_line b ON b.parent_id = p.id
    WHERE w.depth < :max_depth
)
SELECT
    COUNT(*),
    SUM(i.id IS NULL),
    SUM(CASE WHEN i.kind = 'made' AND i.labour_cost IS NULL THEN 1
             WHEN i.kind = 'bought' AND i.std_cost IS NULL THEN 1 ELSE 0 END),
    SUM(w.depth = :max_depth AND i.kind = 'made'
        AND EXISTS (SELECT 1 FROM bom_line x WHERE x.parent_id = w.item_id)),
    SUM(w.mult * CASE i.kind WHEN 'made' THEN i.labour_cost ELSE i.std_cost END)
FROM walk w
LEFT JOIN item i ON i.id = w.item_id
"""


def rolled_cost(conn, item_id):
    """Rolled-up unit cost of item_id, or None when it cannot be given in full.

    A bought item costs its std_cost. A made item costs its labour_cost plus qty times the rolled
    cost of each of its components. Finance's rule: if anything anywhere under the item is missing
    from the item table (the BOM lines purged from the ERP in spring still point at such items),
    the item gets no cost at all, never a partial total. None is also returned for an unknown
    item_id, for a cost that is NULL where one is needed, and for a BOM that is deeper than
    MAX_DEPTH levels (a cycle).
    """
    rows, missing, no_cost, too_deep, total = conn.execute(
        _ROLLUP_SQL, {"item_id": item_id, "max_depth": MAX_DEPTH}
    ).fetchone()
    if missing or no_cost or too_deep:
        return None
    return total
