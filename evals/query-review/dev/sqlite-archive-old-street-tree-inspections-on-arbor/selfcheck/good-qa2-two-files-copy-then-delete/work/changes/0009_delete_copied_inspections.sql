-- ticket: TREE-340 step 2: delete the copied inspections from edges
DELETE FROM edges WHERE id IN (SELECT e.id FROM edges e JOIN archive_edges a ON a.id = e.id WHERE e.kind = 'inspected' LIMIT 900);
