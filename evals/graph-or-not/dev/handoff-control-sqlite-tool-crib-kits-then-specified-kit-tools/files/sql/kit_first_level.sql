SELECT i.id, i.code, i.kind, l.qty
FROM kit_line l JOIN crib_item i ON i.id = l.item_id
WHERE l.kit_id = :kit_id
ORDER BY i.code;
