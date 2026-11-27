-- People currently assigned to each unit (direct assignments only), for :as_of.
SELECT u.id, u.name, COUNT(a.id) AS people
FROM unit u
LEFT JOIN assignment a ON a.unit_id = u.id
  AND a.start_date <= :as_of AND (a.end_date IS NULL OR a.end_date >= :as_of)
GROUP BY u.id, u.name
ORDER BY u.name;
