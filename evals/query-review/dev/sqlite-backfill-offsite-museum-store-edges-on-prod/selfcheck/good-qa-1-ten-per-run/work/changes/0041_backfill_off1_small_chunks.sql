-- ticket: backfill OFF-1 located_in edges, 10 objects per run
-- reviewer:
INSERT INTO edges (kind, src, dst, since)
SELECT 'located_in', o.id, l.id, o.moved_on
FROM nodes o JOIN nodes l ON l.code = 'OFF-1'
LEFT JOIN edges e ON e.src = o.id AND e.kind = 'located_in'
WHERE o.kind = 'object' AND o.location_code = 'OFF-1' AND e.id IS NULL
LIMIT 10;
