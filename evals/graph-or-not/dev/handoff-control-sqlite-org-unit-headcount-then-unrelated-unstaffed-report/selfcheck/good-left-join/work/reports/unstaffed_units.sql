SELECT u.id, u.name
FROM unit AS u
LEFT JOIN assignment AS a
  ON a.unit_id = u.id AND a.start_date <= :as_of AND COALESCE(a.end_date, '9999-12-31') >= :as_of
WHERE u.opened_on <= :as_of AND COALESCE(u.closed_on, '9999-12-31') >= :as_of
GROUP BY u.id, u.name
HAVING COUNT(a.id) = 0
