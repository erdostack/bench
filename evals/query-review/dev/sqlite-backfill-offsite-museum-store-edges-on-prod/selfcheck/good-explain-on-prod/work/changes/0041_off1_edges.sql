-- ticket: backfill located_in for OFF-1
-- reviewer:
INSERT INTO edges (kind, src, dst, since)
SELECT 'located_in', o.id, off.id, o.moved_on
FROM nodes o JOIN nodes off ON off.code = 'OFF-1'
LEFT JOIN edges e ON e.src = o.id AND e.dst = off.id AND e.kind = 'located_in'
WHERE o.kind = 'object' AND o.location_code = 'OFF-1' AND e.id IS NULL
ORDER BY o.id
LIMIT 400;
