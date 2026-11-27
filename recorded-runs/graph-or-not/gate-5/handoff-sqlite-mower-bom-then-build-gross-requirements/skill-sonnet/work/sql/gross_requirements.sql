-- Gross requirements: every bought-in part (make_buy = 'B') needed to make :qty of :item_id.
-- Walks bom_line down from the item. Each BOM line adds 4% scrap, compounding per level
-- (docs/graph/DECISION.md). One row per route, summed per part. Depth guard of 12 levels
-- (deepest BOM is 11) so a cycle in the data cannot loop forever.
WITH RECURSIVE walk (item_id, need, depth) AS (
    SELECT i.id, 1.0 * :qty, 0
    FROM item i
    WHERE i.id = :item_id
    UNION ALL
    SELECT b.component_id, w.need * b.qty_per * 1.04, w.depth + 1
    FROM walk w
    JOIN bom_line b ON b.parent_id = w.item_id
    WHERE w.depth < 12
)
SELECT w.item_id, SUM(w.need) AS need
FROM walk w
JOIN item i ON i.id = w.item_id
WHERE i.make_buy = 'B'
GROUP BY w.item_id
ORDER BY w.item_id;
