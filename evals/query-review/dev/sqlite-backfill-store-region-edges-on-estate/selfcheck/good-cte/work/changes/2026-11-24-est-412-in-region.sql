-- why: EST-412 backfill in_region for operated stores
WITH missing AS (
  SELECT s.id AS store, s.region_code, s.opened_on FROM nodes s
  WHERE s.kind = 'store' AND s.status <> 'closed' AND s.status <> 'planning'
    AND s.id NOT IN (SELECT src FROM edges WHERE kind = 'in_region')
  ORDER BY s.id LIMIT 250
)
INSERT INTO edges (kind, src, dst, since)
SELECT 'in_region', m.store, r.id, m.opened_on FROM missing m JOIN nodes r ON r.kind = 'region' AND r.code = m.region_code;
