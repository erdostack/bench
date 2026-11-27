-- MED-4412: small chunks
INSERT INTO edges (kind, src, dst, since)
SELECT 'covered_by', d.id, k.id, '2026-12-01'
FROM nodes d
JOIN edges m ON m.src = d.id AND m.kind = 'made_by'
JOIN nodes v ON v.id = m.dst AND v.code = 'V-HALVARD'
JOIN nodes k ON k.code = 'SC-2027-ANA'
LEFT JOIN edges c ON c.src = d.id AND c.kind = 'covered_by' AND c.dst = k.id
WHERE d.kind = 'device' AND d.class = 'anaesthesia' AND d.status NOT IN ('loan', 'condemned') AND c.id IS NULL
LIMIT 10;
