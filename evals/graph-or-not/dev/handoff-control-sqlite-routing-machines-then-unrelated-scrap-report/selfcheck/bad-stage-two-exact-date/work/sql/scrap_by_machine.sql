-- Scrap report for :day: non-void rows only, machines with at least one such row.
SELECT machine_id, SUM(produced) AS produced, SUM(scrapped) AS scrapped
FROM prod_log
WHERE logged_at = :day AND status <> 'void'
GROUP BY machine_id
ORDER BY machine_id;
