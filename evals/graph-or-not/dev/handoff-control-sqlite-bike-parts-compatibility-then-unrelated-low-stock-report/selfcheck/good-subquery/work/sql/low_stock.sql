select id as part_id, sku, ifnull((select on_hand from stock where stock.part_id = part.id and store_id = :store_id), 0) as on_hand, reorder_level
from part
where ifnull((select on_hand from stock where stock.part_id = part.id and store_id = :store_id), 0) < reorder_level
order by sku
