-- why: PROG-2026-11 cut-off: episodes aired before 2024-01-01 go to the archive, edges at either end first (docs/archive.md)
INSERT INTO edges_archive SELECT e.* FROM edges e WHERE e.id IN (
  SELECT x.id FROM edges x JOIN nodes n ON n.id IN (x.src, x.dst)
  WHERE n.kind = 'episode' AND n.aired_on < '2024-01-01' ORDER BY x.id LIMIT 600)
  AND NOT EXISTS (SELECT 1 FROM edges_archive a WHERE a.id = e.id);
DELETE FROM edges WHERE id IN (SELECT id FROM edges_archive);
INSERT INTO nodes_archive SELECT n.* FROM nodes n WHERE n.kind = 'episode' AND n.aired_on < '2024-01-01'
  AND (SELECT count(*) FROM edges e WHERE e.src = n.id OR e.dst = n.id) = 0
  AND n.id IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 200);
DELETE FROM nodes WHERE id IN (SELECT id FROM nodes_archive)
