INSERT INTO edges (kind, src, dst, since)
SELECT 'covered_by', d.id, (SELECT id FROM nodes WHERE code = 'SC-2027-ANA'), '2026-12-01'
FROM nodes d JOIN edges m ON m.src = d.id AND m.kind = 'made_by'
WHERE d.kind = 'device' AND d.class = 'anaesthesia'
  AND m.dst = (SELECT id FROM nodes WHERE code = 'V-HALVARD');
