-- why: OPS-2xx, the September brochure import made PU-1187, a second node for Leeds Coach Station Bay 3 (PU-0412). Re-point its edges to PU-0412, then delete it (docs/pickups.md).
INSERT INTO edges (kind, src, dst)
SELECT kind, src, (SELECT id FROM nodes WHERE code = 'PU-0412') FROM edges WHERE dst = (SELECT id FROM nodes WHERE code = 'PU-1187') ORDER BY id LIMIT 150;
DELETE FROM edges WHERE dst = (SELECT id FROM nodes WHERE code = 'PU-1187')
  AND EXISTS (SELECT 1 FROM edges n WHERE n.kind = edges.kind AND n.src = edges.src AND n.dst = (SELECT id FROM nodes WHERE code = 'PU-0412'));
DELETE FROM nodes WHERE code = 'PU-1187' AND NOT EXISTS (SELECT 1 FROM edges WHERE dst = (SELECT id FROM nodes WHERE code = 'PU-1187'));
