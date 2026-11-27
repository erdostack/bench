-- Connections panel: routes you can catch at :stop_id or at the stop across the road, without
-- school-only routes. The export records each pair once, on one stop only, so look both ways.
SELECT DISTINCT r.route_id, r.short_name
FROM stop_route sr
JOIN route r ON r.route_id = sr.route_id
WHERE r.school_only = 0
  AND (sr.stop_id = :stop_id
       OR sr.stop_id IN (SELECT paired_stop_id FROM stop WHERE stop_id = :stop_id AND paired_stop_id IS NOT NULL)
       OR sr.stop_id IN (SELECT stop_id FROM stop WHERE paired_stop_id = :stop_id))
ORDER BY r.short_name;
