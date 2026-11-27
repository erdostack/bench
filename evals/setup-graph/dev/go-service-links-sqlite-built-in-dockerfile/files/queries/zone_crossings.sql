-- Direct links that cross a zone boundary, slowest first.
SELECT a.zone AS from_zone, b.zone AS to_zone, l.from_stop, l.to_stop, l.minutes
FROM link AS l
JOIN stop AS a ON a.id = l.from_stop
JOIN stop AS b ON b.id = l.to_stop
WHERE a.zone <> b.zone
ORDER BY l.minutes DESC
LIMIT 20;
