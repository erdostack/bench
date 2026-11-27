-- MED-4412: SC-2027-ANA cover for our Halvard anaesthesia machines (loan/condemned excluded, pilot already done)
INSERT INTO edges (kind, src, dst, since)
SELECT 'covered_by', d.id, k.id, '2026-12-01'
FROM nodes d
JOIN edges m ON m.src = d.id AND m.kind = 'made_by'
JOIN nodes v ON v.id = m.dst AND v.code = 'V-HALVARD'
JOIN nodes k ON k.code = 'SC-2027-ANA'
WHERE d.kind = 'device' AND d.class = 'anaesthesia' AND d.status NOT IN ('loan', 'condemned')
  AND d.id NOT IN (SELECT src FROM edges WHERE kind = 'covered_by' AND dst = k.id)
ORDER BY d.id
LIMIT 250;
