-- ticket: TREE-340 archive inspections of trees removed before 2024-01-01 (tablet history is slow)
-- reviewed-by:
INSERT INTO archive_edges
SELECT * FROM edges WHERE kind = 'inspected'
  AND dst IN (SELECT id FROM nodes WHERE kind = 'tree' AND status = 'removed' AND removed_on < date('2024-01-01'))
ORDER BY id LIMIT 25;
DELETE FROM edges WHERE id IN (SELECT a.id FROM archive_edges a JOIN edges e ON e.id = a.id);
