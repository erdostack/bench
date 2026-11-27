-- ticket: TREE-340 also trees removed in 2024
INSERT INTO archive_edges SELECT * FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'inspected' AND dst IN (SELECT id FROM nodes WHERE kind = 'tree' AND status = 'removed' AND removed_on < '2025-01-01') AND id NOT IN (SELECT id FROM archive_edges) LIMIT 400);
DELETE FROM edges WHERE kind = 'inspected' AND id IN (SELECT id FROM archive_edges);
