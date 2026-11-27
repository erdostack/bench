-- People currently assigned to each unit including all units below it, for :as_of.
-- A person assigned to several units inside one subtree is counted once for that unit.
WITH RECURSIVE tree(root_id, unit_id) AS (
    SELECT id, id FROM unit
    UNION ALL
    SELECT t.root_id, u.id FROM tree t JOIN unit u ON u.parent_id = t.unit_id
)
SELECT r.id, r.name, COUNT(DISTINCT a.person_id) AS people
FROM unit r
JOIN tree t ON t.root_id = r.id
LEFT JOIN assignment a ON a.unit_id = t.unit_id
  AND a.start_date <= :as_of AND (a.end_date IS NULL OR a.end_date >= :as_of)
GROUP BY r.id, r.name
ORDER BY r.name;
