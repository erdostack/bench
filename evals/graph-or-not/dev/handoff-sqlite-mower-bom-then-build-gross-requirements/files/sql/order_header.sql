SELECT w.id, w.qty, w.due, i.part_no, i.description
FROM works_order w JOIN item i ON i.id = w.item_id
WHERE w.id = :order_id;
