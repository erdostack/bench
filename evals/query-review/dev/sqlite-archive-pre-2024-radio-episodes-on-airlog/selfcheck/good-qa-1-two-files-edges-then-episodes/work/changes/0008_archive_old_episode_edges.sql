-- why: 2026 cut-off (before 2024-01-01), step 1 of 2, the edges at either end, 900 a run
INSERT OR IGNORE INTO edges_archive SELECT e.* FROM edges e JOIN nodes n ON n.id IN (e.src, e.dst)
  WHERE n.kind = 'episode' AND n.aired_on < '2024-01-01' AND e.id IN (
    SELECT e2.id FROM edges e2 JOIN nodes n2 ON n2.id IN (e2.src, e2.dst) WHERE n2.kind = 'episode' AND n2.aired_on < '2024-01-01' ORDER BY e2.id LIMIT 900);
DELETE FROM edges WHERE id IN (SELECT id FROM edges_archive);
