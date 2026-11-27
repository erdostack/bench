"""Gross requirements: bought-in parts for qty of an item, all the way down the BOM.

Scrap: 4% added to each part's total."""
SCRAP = 0.04

QUERY = """
WITH RECURSIVE need(item_id, qty) AS (
    SELECT b.component_id, :qty * b.qty_per
    FROM bom_line b WHERE b.parent_id = :item_id
    UNION ALL
    SELECT b.component_id, n.qty * b.qty_per
    FROM need n
    JOIN item i ON i.id = n.item_id AND i.make_buy = 'M'
    JOIN bom_line b ON b.parent_id = n.item_id
)
SELECT n.item_id, ROUND(SUM(n.qty) * (1 + :scrap), 3)
FROM need n JOIN item i ON i.id = n.item_id
WHERE i.make_buy = 'B'
GROUP BY n.item_id
"""


def gross_requirements(conn, item_id, qty):
    rows = conn.execute(QUERY, {"item_id": item_id, "qty": qty, "scrap": SCRAP}).fetchall()
    return {part: amount for part, amount in rows}
