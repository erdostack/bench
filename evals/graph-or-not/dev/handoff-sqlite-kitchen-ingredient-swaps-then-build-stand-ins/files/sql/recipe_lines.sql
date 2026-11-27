SELECT i.id, i.name, l.qty, i.unit
FROM recipe_line l JOIN ingredient i ON i.id = l.ingredient_id
WHERE l.recipe_id = :recipe_id
ORDER BY l.position;
