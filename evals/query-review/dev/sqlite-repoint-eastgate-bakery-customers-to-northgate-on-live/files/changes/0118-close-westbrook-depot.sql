-- ticket: OPS-201 Westbrook closed; its customers moved to Southmead in chunks of 400
UPDATE edges SET dst = (SELECT id FROM nodes WHERE ref = 'DEP-SOUTHMEAD')
WHERE id IN (
    SELECT id FROM edges
    WHERE kind = 'served_from' AND dst = (SELECT id FROM nodes WHERE ref = 'DEP-WESTBROOK')
    LIMIT 400
);
