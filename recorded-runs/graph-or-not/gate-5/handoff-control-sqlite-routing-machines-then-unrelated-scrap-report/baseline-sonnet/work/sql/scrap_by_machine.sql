SELECT machine_id, SUM(produced) AS produced, SUM(scrapped) AS scrapped
FROM prod_log
WHERE status <> 'void'
  AND logged_at >= :day
  AND logged_at <  date(:day, '+1 day')
GROUP BY machine_id
ORDER BY machine_id;
