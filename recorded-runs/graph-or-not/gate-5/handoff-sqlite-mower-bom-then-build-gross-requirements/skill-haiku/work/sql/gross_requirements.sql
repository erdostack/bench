-- Every bought-in part reached from :item_id, summed over all BOM paths, per one unit of :item_id.
-- Each line on a path multiplies the quantity by qty_per * :line_factor (scrap); the walk stops at :max_depth lines.
WITH RECURSIVE walk (component_id, per_unit, depth) AS (
    SELECT b.component_id, b.qty_per * :line_factor, 1
    FROM bom_line b
    WHERE b.parent_id = :item_id
    UNION ALL
    SELECT b.component_id, w.per_unit * b.qty_per * :line_factor, w.depth + 1
    FROM walk w JOIN bom_line b ON b.parent_id = w.component_id
    WHERE w.depth < :max_depth
)
SELECT w.component_id, SUM(w.per_unit)
FROM walk w JOIN item c ON c.id = w.component_id
WHERE c.make_buy = 'B'
GROUP BY w.component_id
ORDER BY w.component_id;
