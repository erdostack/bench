-- ticket: OPS-233 Eastgate closes, its customers are served from Northgate, 450 per run (limit 500)
UPDATE edges SET dst = (SELECT id FROM nodes WHERE ref = 'DEP-NORTHGATE')
WHERE id IN (
    SELECT id FROM edges
    WHERE kind = 'served_from' AND dst = (SELECT id FROM nodes WHERE ref = 'DEP-EASTGATE')
    LIMIT 450
);
