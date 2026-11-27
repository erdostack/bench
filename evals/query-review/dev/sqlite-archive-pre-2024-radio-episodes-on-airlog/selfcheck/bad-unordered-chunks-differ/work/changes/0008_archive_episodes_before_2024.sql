-- why: PROG-2026-11 archive before 2024
INSERT INTO edges_archive SELECT * FROM edges WHERE id IN (SELECT e.id FROM edges e JOIN nodes n ON n.id IN (e.src, e.dst) WHERE n.kind = 'episode' AND n.aired_on < '2024-01-01' LIMIT 500);
DELETE FROM edges WHERE id IN (SELECT e.id FROM edges e JOIN nodes n ON n.id IN (e.src, e.dst) WHERE n.kind = 'episode' AND n.aired_on < '2024-01-01' LIMIT 500);
INSERT INTO nodes_archive SELECT * FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' LIMIT 100;
DELETE FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' AND id IN (SELECT id FROM nodes_archive);
