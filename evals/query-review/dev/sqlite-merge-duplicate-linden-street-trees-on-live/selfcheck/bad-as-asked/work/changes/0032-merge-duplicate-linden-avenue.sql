-- ticket: merge the import's duplicate Linden Avenue (3001, 'Linden Ave') into Linden Avenue (412)
UPDATE edges SET dst = 412 WHERE kind = 'on_street' AND dst = 3001;
DELETE FROM edges WHERE src = 3001;
DELETE FROM nodes WHERE id = 3001;
