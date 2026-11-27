-- why: PROG-2025-11 committee cut-off, episodes aired before 2022-01-01 go to the archive (30 episodes a run)
INSERT INTO edges_archive SELECT * FROM edges WHERE src IN (
    SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2022-01-01' ORDER BY id LIMIT 30);
DELETE FROM edges WHERE src IN (
    SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2022-01-01' ORDER BY id LIMIT 30);
INSERT INTO nodes_archive SELECT * FROM nodes WHERE id IN (
    SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2022-01-01' ORDER BY id LIMIT 30);
DELETE FROM nodes WHERE id IN (
    SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2022-01-01' ORDER BY id LIMIT 30);
