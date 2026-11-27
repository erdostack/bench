-- why: EST-412
INSERT INTO edges (kind, src, dst, since)
SELECT 'in_region', s.id, r.id, s.opened_on
FROM nodes s JOIN nodes r ON r.kind = 'region' AND r.code = s.region_code
WHERE s.kind = 'store' AND s.status IN ('trading', 'refit') AND s.code >= 'ST-2300'
LIMIT 400;
