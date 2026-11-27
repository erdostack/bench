-- Connections panel: the routes at a stop and at the stop across the road (the export's pair column).
SELECT DISTINCT r.route_id, r.short_name
FROM stop_route sr
JOIN route r ON r.route_id = sr.route_id
WHERE sr.stop_id IN (
        SELECT :stop_id
        UNION SELECT paired_stop_id FROM stop WHERE stop_id = :stop_id
        UNION SELECT stop_id FROM stop WHERE paired_stop_id = :stop_id
  )
  AND r.school_only = 0   -- customer services: school-only routes aren't shown
ORDER BY r.short_name;
