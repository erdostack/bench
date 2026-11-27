-- ticket: OPS-233
UPDATE edges SET dst = (SELECT id FROM nodes WHERE ref = 'DEP-NORTHGATE') WHERE kind = 'served_from' AND dst = (SELECT id FROM nodes WHERE ref = 'DEP-EASTGATE');
