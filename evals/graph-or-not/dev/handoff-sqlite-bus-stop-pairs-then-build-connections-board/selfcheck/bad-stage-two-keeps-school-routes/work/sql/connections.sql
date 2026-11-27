SELECT DISTINCT r.route_id, r.short_name
FROM stop_route sr
JOIN route r ON r.route_id = sr.route_id
WHERE sr.stop_id = :stop_id
   OR sr.stop_id = (SELECT paired_stop_id FROM stop WHERE stop_id = :stop_id)
   OR sr.stop_id IN (SELECT stop_id FROM stop WHERE paired_stop_id = :stop_id);
