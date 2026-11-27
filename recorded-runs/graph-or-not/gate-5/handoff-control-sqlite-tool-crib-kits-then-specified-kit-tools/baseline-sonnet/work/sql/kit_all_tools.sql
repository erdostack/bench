-- Every tool in a kit, including tools in kits packed inside it.
-- qty is multiplied down the nesting. Depth guard stops a bad cycle in the data.
WITH RECURSIVE contents (item_id, qty, depth) AS (
    SELECT l.item_id, l.qty, 1
    FROM kit_line l
    WHERE l.kit_id = :kit_id
    UNION ALL
    SELECT l.item_id, c.qty * l.qty, c.depth + 1
    FROM contents c
    JOIN crib_item k ON k.id = c.item_id AND k.kind = 'kit'
    JOIN kit_line l ON l.kit_id = k.id
    WHERE c.depth < 8
)
SELECT i.id, i.code, i.title, SUM(c.qty) AS qty
FROM contents c JOIN crib_item i ON i.id = c.item_id
WHERE i.kind = 'tool'
GROUP BY i.id, i.code, i.title
ORDER BY i.code;
