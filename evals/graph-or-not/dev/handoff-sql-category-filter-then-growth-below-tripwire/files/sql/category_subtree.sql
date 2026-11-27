-- Category filter: the chosen category and every category below it.
WITH RECURSIVE sub AS (
    SELECT id FROM category WHERE id = $1
    UNION ALL
    SELECT c.id FROM category c JOIN sub ON c.parent_id = sub.id
)
SELECT p.id, p.title, p.price_cents
FROM product p
JOIN sub ON p.category_id = sub.id
WHERE p.listed
ORDER BY p.rank DESC
LIMIT $2;
