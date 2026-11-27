-- Gross requirements for :qty of item :item_id: every bought-in part, all the way down the BOM.
-- 4% scrap is added on every BOM line, so it compounds with depth: a part three levels down carries
-- 1.04 ^ 3. The order quantity itself gets no scrap. A part used on several paths is summed.
-- Only made items ('M') are expanded; bought items ('B') are leaves. The depth cap (BOMs are at most
-- 11 levels deep) is a backstop against a loop in the PLM data.
WITH RECURSIVE walk (item_id, make_buy, required, depth) AS (
    SELECT i.id, i.make_buy, CAST(:qty AS DOUBLE PRECISION), 0
    FROM item i
    WHERE i.id = :item_id
  UNION ALL
    SELECT c.id, c.make_buy, w.required * b.qty_per * 1.04, w.depth + 1
    FROM walk w
    JOIN bom_line b ON b.parent_id = w.item_id
    JOIN item c ON c.id = b.component_id
    WHERE w.make_buy = 'M' AND w.depth < 25
)
SELECT i.id, i.part_no, i.description, i.uom, SUM(w.required) AS required
FROM walk w JOIN item i ON i.id = w.item_id
WHERE w.make_buy = 'B'
GROUP BY i.id, i.part_no, i.description, i.uom
ORDER BY i.part_no;
