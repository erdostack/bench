-- MED-4120: Corvane infusion pumps under SC-2026-INF from 2026-10-01 (reviewed: p.nwosu, applied 2026-09-30)
INSERT INTO edges (kind, src, dst, since)
SELECT 'covered_by', d.id, (SELECT id FROM nodes WHERE code = 'SC-2026-INF'), '2026-10-01'
FROM nodes d
WHERE d.kind = 'device' AND d.class = 'infusion' AND d.status IN ('in_service', 'in_store')
  AND d.id IN (SELECT src FROM edges WHERE kind = 'made_by' AND dst = (SELECT id FROM nodes WHERE code = 'V-CORVANE'))
  AND NOT EXISTS (SELECT 1 FROM edges c WHERE c.kind = 'covered_by' AND c.src = d.id
                  AND c.dst = (SELECT id FROM nodes WHERE code = 'SC-2026-INF'))
LIMIT 400;
