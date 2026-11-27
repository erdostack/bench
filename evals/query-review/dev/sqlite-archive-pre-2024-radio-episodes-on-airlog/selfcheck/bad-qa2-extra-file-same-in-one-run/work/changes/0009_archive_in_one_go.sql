-- why: the same archive in one run, for a quiet night
INSERT INTO edges_archive SELECT * FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01') OR dst IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01');
DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01') OR dst IN (SELECT id FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01');
INSERT INTO nodes_archive SELECT * FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01';
DELETE FROM nodes WHERE kind = 'episode' AND aired_on < '2024-01-01'
