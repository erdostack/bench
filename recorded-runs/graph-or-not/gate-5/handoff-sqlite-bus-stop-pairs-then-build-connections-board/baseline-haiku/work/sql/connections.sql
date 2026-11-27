-- Connections panel: routes calling at the stop on the other side of the road from :stop_id, one row per route.
-- The export records each pair once, on one of the two stops, so match the pair in both directions.
WITH partner(stop_id) AS (
    SELECT paired_stop_id FROM stop WHERE stop_id = :stop_id AND paired_stop_id IS NOT NULL
    UNION
    SELECT stop_id FROM stop WHERE paired_stop_id = :stop_id
)
SELECT DISTINCT r.route_id, r.short_name
FROM partner p
JOIN stop_route sr ON sr.stop_id = p.stop_id
JOIN route r ON r.route_id = sr.route_id
ORDER BY r.short_name;
