SELECT c.id, c.part_no, c.description, b.qty_per, c.make_buy
FROM bom_line b JOIN item c ON c.id = b.component_id
WHERE b.parent_id = :item_id
ORDER BY c.part_no;
