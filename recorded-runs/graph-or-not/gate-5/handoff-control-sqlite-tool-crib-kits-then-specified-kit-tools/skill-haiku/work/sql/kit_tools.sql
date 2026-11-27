-- Every tool inside :kit_id at any depth, with quantities multiplied down
-- the nesting and summed across all routes to the same tool.
-- Sub-kits are walked through but not returned. SQLite.

WITH RECURSIVE walk(item_id, qty) AS (
    SELECT l.item_id, l.qty
    FROM kit_line AS l
    WHERE l.kit_id = :kit_id
    UNION ALL
    SELECT l.item_id, w.qty * l.qty
    FROM walk AS w
    JOIN kit_line AS l ON l.kit_id = w.item_id
)
SELECT i.id AS tool_id, SUM(w.qty) AS qty
FROM walk AS w
JOIN crib_item AS i ON i.id = w.item_id
WHERE i.kind = 'tool'
GROUP BY i.id
ORDER BY i.id;
