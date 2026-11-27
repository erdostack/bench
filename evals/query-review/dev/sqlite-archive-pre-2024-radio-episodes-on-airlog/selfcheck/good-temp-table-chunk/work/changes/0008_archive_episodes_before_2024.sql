-- why: PROG-2026-11 archive cut-off 2024-01-01, 25 episodes a run
CREATE TEMP TABLE IF NOT EXISTS chunk (id INTEGER PRIMARY KEY);
DELETE FROM chunk;
INSERT INTO chunk SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 25;
INSERT INTO edges_archive SELECT * FROM edges WHERE src IN (SELECT id FROM chunk) OR dst IN (SELECT id FROM chunk);
DELETE FROM edges WHERE src IN (SELECT id FROM chunk) OR dst IN (SELECT id FROM chunk);
INSERT INTO nodes_archive SELECT * FROM nodes WHERE id IN (SELECT id FROM chunk);
DELETE FROM nodes WHERE id IN (SELECT id FROM chunk);
