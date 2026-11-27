-- Parts below their reorder level at a store. :store_id
SELECT p.id AS part_id, p.sku, coalesce(s.on_hand, 0) AS on_hand, p.reorder_level
FROM part AS p
JOIN stock AS s ON s.part_id = p.id AND s.store_id = :store_id
WHERE coalesce(s.on_hand, 0) < p.reorder_level
ORDER BY p.sku;
