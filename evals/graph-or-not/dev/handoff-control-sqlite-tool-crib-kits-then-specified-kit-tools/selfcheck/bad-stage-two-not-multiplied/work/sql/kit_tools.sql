-- Every tool in :kit_id at any depth; quantities multiply down the nesting and add up across sub-kits.
WITH RECURSIVE inside(item_id, qty) AS (
    SELECT item_id, qty FROM kit_line WHERE kit_id = :kit_id
    UNION ALL
    SELECT l.item_id, l.qty
    FROM inside i JOIN kit_line l ON l.kit_id = i.item_id
)
SELECT n.item_id AS tool_id, SUM(n.qty) AS qty
FROM inside n JOIN crib_item c ON c.id = n.item_id
WHERE c.kind = 'tool'
GROUP BY n.item_id
ORDER BY n.item_id;
