SELECT DISTINCT r.route_id, r.short_name
FROM stop s
JOIN stop_route sr ON sr.stop_id IN (s.stop_id, s.paired_stop_id)
JOIN route r ON r.route_id = sr.route_id
WHERE s.stop_id = :stop_id AND r.school_only = 0;
