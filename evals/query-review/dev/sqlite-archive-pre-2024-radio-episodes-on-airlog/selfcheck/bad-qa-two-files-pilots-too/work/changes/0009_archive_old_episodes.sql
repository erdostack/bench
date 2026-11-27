-- why: 2026 cut-off (before 2024-01-01), step 2 of 2, the episodes once their edges are archived, 500 a run
INSERT INTO nodes_archive SELECT * FROM nodes WHERE id IN (SELECT id FROM nodes WHERE kind = 'episode' AND (aired_on < '2024-01-01' OR aired_on IS NULL) ORDER BY id LIMIT 500);
DELETE FROM nodes WHERE id IN (SELECT id FROM nodes_archive);
