-- MED-4412: Halvard anaesthesia machines under SC-2027-ANA from 2026-12-01 (pattern of the 20260930 file), 10 per run
INSERT INTO edges (kind, src, dst, since)
SELECT 'covered_by', d.id, (SELECT id FROM nodes WHERE code = 'SC-2027-ANA'), '2026-12-01'
FROM nodes d
WHERE d.kind = 'device' AND d.class = 'anaesthesia' AND d.status IN ('in_service', 'in_store')
  AND d.id IN (SELECT src FROM edges WHERE kind = 'made_by' AND dst = (SELECT id FROM nodes WHERE code = 'V-HALVARD'))
  AND NOT EXISTS (SELECT 1 FROM edges c WHERE c.kind = 'covered_by' AND c.src = d.id
                  AND c.dst = (SELECT id FROM nodes WHERE code = 'SC-2027-ANA'))
LIMIT 10;
