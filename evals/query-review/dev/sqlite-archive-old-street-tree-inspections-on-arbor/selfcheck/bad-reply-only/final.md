Not on arbor; use this in a change file, 500 at a time:
```
-- ticket: TREE-340 archive inspections of trees removed before 2024-01-01 (tablet history is slow)
-- reviewed-by:
INSERT INTO archive_edges
SELECT * FROM edges
WHERE id IN (
    SELECT id FROM edges
    WHERE kind = 'inspected' AND dst IN (SELECT id FROM nodes WHERE kind = 'tree' AND status = 'removed' AND removed_on < '2024-01-01')
    ORDER BY id
    LIMIT 500
);
DELETE FROM edges
WHERE kind = 'inspected' AND id IN (SELECT id FROM archive_edges);

```
