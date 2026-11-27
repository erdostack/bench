-- Connections for the stop screen: every non-school route that calls at :stop_id or at the stop across
-- the road, one row per route. The pair is recorded on one stop only, so the partner is found both ways.
WITH here(stop_id) AS (
    SELECT :stop_id
    UNION
    SELECT paired_stop_id FROM stop WHERE stop_id = :stop_id AND paired_stop_id IS NOT NULL
    UNION
    SELECT stop_id FROM stop WHERE paired_stop_id = :stop_id
)
SELECT DISTINCT r.route_id, r.short_name
FROM here h
JOIN stop_route sr ON sr.stop_id = h.stop_id
JOIN route r ON r.route_id = sr.route_id
WHERE r.school_only = 0
ORDER BY r.short_name;
