-- Scrap report for :day: non-void rows only, machines with at least one such row.
SELECT machine_id, SUM(produced) AS produced, SUM(scrapped) AS scrapped
FROM prod_log
WHERE substr(logged_at, 1, 10) = :day
GROUP BY machine_id
ORDER BY machine_id;
