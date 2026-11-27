-- the kit's tools, any depth (multiply down, sum across sub-kits)
WITH RECURSIVE inside(kit, item_id, qty) AS (
    SELECT kit_id, item_id, qty FROM kit_line WHERE kit_id = :kit_id
    UNION ALL
    SELECT l.kit_id, l.item_id, l.qty * i.qty
    FROM kit_line l JOIN inside i ON l.kit_id = i.item_id
)
SELECT item_id AS tool_id, SUM(qty) AS qty
FROM inside
WHERE item_id IN (SELECT id FROM crib_item WHERE kind = 'tool')
GROUP BY item_id
