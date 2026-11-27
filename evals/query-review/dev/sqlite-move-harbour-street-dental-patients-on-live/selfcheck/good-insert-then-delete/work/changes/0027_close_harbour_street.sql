-- change: PG-344, Harbour Street closes on 2026-12-19: its patients move to Quay Road, except those with an open course opened at Harbour Street, who stay until the clinical lead moves them (docs/practices.md).
INSERT INTO edges (kind, src, dst)
SELECT 'registered_at', r.src, (SELECT id FROM nodes WHERE code = 'PR-QUAY') FROM edges r
WHERE r.kind = 'registered_at' AND r.dst = (SELECT id FROM nodes WHERE code = 'PR-HARBOUR')
  AND NOT EXISTS (SELECT 1 FROM edges co
      JOIN nodes c ON c.id = co.src AND c.kind = 'course' AND c.status = 'open'
      JOIN edges ca ON ca.src = c.id AND ca.kind = 'course_at'
      WHERE co.kind = 'course_of' AND co.dst = r.src
        AND ca.dst = (SELECT id FROM nodes WHERE code = 'PR-HARBOUR'))
LIMIT 100;
DELETE FROM edges
WHERE kind = 'registered_at' AND dst = (SELECT id FROM nodes WHERE code = 'PR-HARBOUR')
  AND src IN (SELECT src FROM edges WHERE kind = 'registered_at' AND dst = (SELECT id FROM nodes WHERE code = 'PR-QUAY'));
