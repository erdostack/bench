-- Every tool inside a kit at any depth, as (tool_id, qty).
-- qty is multiplied down the nesting and summed where a tool appears in several places.
-- Kits are walked but not listed. No depth guard: kits cannot contain themselves
-- (enforced by the crib app), and a fixed limit would silently drop deeper tools.
WITH RECURSIVE contents (item_id, qty) AS (
    SELECT l.item_id, l.qty
    FROM kit_line l
    WHERE l.kit_id = :kit_id
    UNION ALL
    SELECT l.item_id, c.qty * l.qty
    FROM contents c
    JOIN kit_line l ON l.kit_id = c.item_id
)
SELECT i.id AS tool_id, SUM(c.qty) AS qty
FROM contents c
JOIN crib_item i ON i.id = c.item_id AND i.kind = 'tool'
GROUP BY i.id
ORDER BY i.id;
