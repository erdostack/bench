-- Tools inside :kit_id at any depth, with quantities multiplied down the nesting
-- and summed where the same tool appears in several places. Sub-kits are not listed.
WITH RECURSIVE tree(item_id, qty) AS (
    SELECT l.item_id, l.qty
    FROM kit_line AS l
    WHERE l.kit_id = :kit_id
    UNION ALL
    SELECT l.item_id, t.qty * l.qty
    FROM tree AS t
    JOIN kit_line AS l ON l.kit_id = t.item_id
)
SELECT t.item_id AS tool_id,
       SUM(t.qty) AS qty
FROM tree AS t
JOIN crib_item AS i ON i.id = t.item_id
WHERE i.kind = 'tool'
GROUP BY t.item_id
ORDER BY t.item_id;
