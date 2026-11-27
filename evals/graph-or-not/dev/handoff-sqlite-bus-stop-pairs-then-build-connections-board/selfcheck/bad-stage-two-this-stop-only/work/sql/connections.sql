SELECT r.route_id, r.short_name
FROM stop_route sr JOIN route r ON r.route_id = sr.route_id
WHERE sr.stop_id = :stop_id AND r.school_only = 0;
