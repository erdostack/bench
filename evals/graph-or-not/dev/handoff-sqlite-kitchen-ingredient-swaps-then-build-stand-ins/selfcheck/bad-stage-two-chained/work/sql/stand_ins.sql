WITH RECURSIVE s(id) AS (
    SELECT item_a FROM swap WHERE item_b = :ingredient_id
    UNION
    SELECT w.item_a FROM swap w JOIN s ON w.item_b = s.id
)
SELECT i.id AS ingredient_id, i.name
FROM ingredient i
WHERE i.id IN (SELECT id FROM s) AND i.id <> :ingredient_id
ORDER BY i.name;
