-- ticket: OFF-1 objects have no located_in edge (docs/model.md, "The OFF-1 move"), conservation cannot see them
-- reviewer:
INSERT INTO edges (kind, src, dst, since)
SELECT 'located_in', o.id, (SELECT id FROM nodes WHERE code = 'OFF-1'), o.moved_on
FROM nodes o
WHERE o.kind = 'object' AND o.location_code = 'OFF-1'
  AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.kind = 'located_in' AND e.src = o.id)
;
