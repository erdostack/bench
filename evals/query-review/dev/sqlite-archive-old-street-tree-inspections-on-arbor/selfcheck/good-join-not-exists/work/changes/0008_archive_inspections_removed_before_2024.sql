-- ticket: TREE-340 archive inspections of trees removed before 2024-01-01 (tablet history is slow)
-- reviewed-by:
INSERT INTO archive_edges
SELECT e.* FROM edges e JOIN nodes t ON t.id = e.dst
WHERE e.kind = 'inspected' AND t.kind = 'tree' AND t.status = 'removed' AND t.removed_on < '2024-01-01'
  AND NOT EXISTS (SELECT 1 FROM archive_edges a WHERE a.id = e.id)
LIMIT 400;
DELETE FROM edges WHERE id IN (
    SELECT e.id FROM edges e JOIN archive_edges a ON a.id = e.id
);
