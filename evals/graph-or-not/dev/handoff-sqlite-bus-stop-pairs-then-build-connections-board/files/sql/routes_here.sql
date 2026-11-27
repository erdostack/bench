-- Routes calling at :stop_id, for the top line of the board.
SELECT r.route_id, r.short_name
FROM stop_route sr
JOIN route r ON r.route_id = sr.route_id
WHERE sr.stop_id = :stop_id
ORDER BY r.short_name;
