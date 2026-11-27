SELECT i.id AS ingredient_id, i.name
FROM swap s JOIN ingredient i ON i.id = s.item_b
WHERE s.item_a = :ingredient_id
ORDER BY i.name;
