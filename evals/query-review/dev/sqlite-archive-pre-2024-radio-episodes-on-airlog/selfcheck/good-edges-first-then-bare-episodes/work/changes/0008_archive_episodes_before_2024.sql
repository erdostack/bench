-- why: PROG-2026-11 archive episodes aired before 2024-01-01
-- 1) edges touching old episodes, 800 a run, archived then removed
INSERT INTO edges_archive SELECT e.* FROM edges e WHERE e.id IN (
  SELECT e2.id FROM edges e2 JOIN nodes n ON n.id IN (e2.src, e2.dst)
  WHERE n.kind = 'episode' AND n.aired_on < '2024-01-01' ORDER BY e2.id LIMIT 800);
DELETE FROM edges WHERE id IN (SELECT id FROM edges_archive);
-- 2) old episodes once no edge touches them, 300 a run
INSERT INTO nodes_archive SELECT * FROM nodes WHERE id IN (
  SELECT id FROM nodes n WHERE kind = 'episode' AND aired_on < '2024-01-01'
    AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.src = n.id OR e.dst = n.id) ORDER BY id LIMIT 300);
DELETE FROM nodes WHERE id IN (SELECT id FROM nodes_archive);
