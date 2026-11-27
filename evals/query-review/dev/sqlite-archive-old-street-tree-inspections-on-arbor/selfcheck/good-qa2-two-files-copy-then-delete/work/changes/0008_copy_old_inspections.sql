-- ticket: TREE-340 step 1: copy inspections of trees removed before 2024 into archive_edges
INSERT OR IGNORE INTO archive_edges
SELECT * FROM edges WHERE id IN (SELECT e.id FROM edges e JOIN nodes t ON t.id = e.dst
  WHERE e.kind = 'inspected' AND t.kind = 'tree' AND t.status = 'removed' AND t.removed_on < '2024-01-01'
    AND e.id NOT IN (SELECT id FROM archive_edges) LIMIT 900);
