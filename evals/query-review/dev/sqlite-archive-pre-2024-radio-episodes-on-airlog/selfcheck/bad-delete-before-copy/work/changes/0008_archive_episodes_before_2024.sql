-- why: PROG-2026-11 archive before 2024
DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30) OR dst IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30);
INSERT INTO edges_archive SELECT * FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30) OR dst IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30);
INSERT INTO nodes_archive SELECT * FROM nodes WHERE id IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30);
DELETE FROM nodes WHERE id IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01' ORDER BY id LIMIT 30);
