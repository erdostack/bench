-- MED-4412: Halvard anaesthesia machines under SC-2027-ANA from 2026-12-01, unindexed scan, 10 per run
INSERT INTO edges (kind, src, dst, since)
SELECT 'covered_by', d.id, (SELECT id FROM nodes WHERE code = 'SC-2027-ANA'), '2026-12-01'
FROM nodes d
WHERE d.kind = 'device' AND d.class = 'anaesthesia' AND d.status IN ('in_service', 'in_store')
  AND d.id IN (SELECT src + 0 FROM edges WHERE kind || '' = 'made_by' AND dst = (SELECT id FROM nodes WHERE code = 'V-HALVARD'))
  AND d.id NOT IN (SELECT c.src + 0 FROM edges c WHERE c.kind || '' = 'covered_by'
                  AND c.dst = (SELECT id FROM nodes WHERE code = 'SC-2027-ANA'))
LIMIT 10;
