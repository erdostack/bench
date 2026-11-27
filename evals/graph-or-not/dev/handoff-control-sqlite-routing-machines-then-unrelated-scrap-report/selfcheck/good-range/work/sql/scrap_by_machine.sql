SELECT machine_id, SUM(produced), SUM(scrapped)
FROM prod_log
WHERE logged_at >= :day AND logged_at < date(:day, '+1 day') AND status = 'ok'
GROUP BY machine_id
ORDER BY machine_id
