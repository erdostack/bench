-- One part. :part_id
SELECT id, sku, name, reorder_level FROM part WHERE id = :part_id;
