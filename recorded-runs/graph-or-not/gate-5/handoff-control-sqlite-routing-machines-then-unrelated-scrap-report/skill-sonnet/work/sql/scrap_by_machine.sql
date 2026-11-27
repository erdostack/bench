-- Scrap report for one day. Parameter: :day ('YYYY-MM-DD').
-- One row per machine with at least one non-void prod_log row that day;
-- void rows are ignored entirely. logged_at is local time, so the day is
-- taken as written, with no timezone conversion.
SELECT machine_id,
       SUM(produced)  AS produced,
       SUM(scrapped)  AS scrapped
FROM prod_log
WHERE status <> 'void'
  AND logged_at >= :day
  AND logged_at <  date(:day, '+1 day')
GROUP BY machine_id
ORDER BY machine_id;
