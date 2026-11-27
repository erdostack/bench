WITH sides(stop_id) AS (
    SELECT :stop_id
    UNION SELECT paired_stop_id FROM stop WHERE stop_id = :stop_id AND paired_stop_id IS NOT NULL
    UNION SELECT stop_id FROM stop WHERE paired_stop_id = :stop_id
)
SELECT r.route_id, r.short_name
FROM route r
WHERE r.school_only = 0
  AND r.route_id IN (SELECT route_id FROM stop_route WHERE stop_id IN (SELECT stop_id FROM sides));
