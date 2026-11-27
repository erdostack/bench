-- Every tool inside a kit at any depth, with total quantity. Parameter: :kit_id.
-- Returns (tool_id, qty). Sub-kits are not listed.
--
-- Quantities multiply down the nesting and add up across routes, so each
-- route is walked separately (UNION ALL, carrying the product of qty) and
-- the routes are summed per tool at the end. Deduplicating items while
-- walking (UNION on item ids) would lose quantities when a tool or sub-kit
-- is packed in more than one place. Kits never contain themselves (enforced
-- by the crib app), so the walk ends at the tools.
WITH RECURSIVE contents(item_id, qty) AS (
    SELECT l.item_id, l.qty
    FROM kit_line AS l
    WHERE l.kit_id = :kit_id
    UNION ALL
    SELECT l.item_id, c.qty * l.qty
    FROM contents AS c
    JOIN kit_line AS l ON l.kit_id = c.item_id
)
SELECT c.item_id AS tool_id,
       SUM(c.qty) AS qty
FROM contents AS c
JOIN crib_item AS i ON i.id = c.item_id
WHERE i.kind = 'tool'
GROUP BY c.item_id
ORDER BY c.item_id;
