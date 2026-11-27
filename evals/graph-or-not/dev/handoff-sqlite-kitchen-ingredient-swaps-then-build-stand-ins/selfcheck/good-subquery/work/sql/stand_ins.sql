SELECT id AS ingredient_id, name
FROM ingredient
WHERE id IN (SELECT item_a FROM swap WHERE item_b = :ingredient_id)
ORDER BY name
