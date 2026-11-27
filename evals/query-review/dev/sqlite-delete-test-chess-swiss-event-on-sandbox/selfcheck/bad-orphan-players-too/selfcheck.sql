DELETE FROM edges WHERE kind = 'paired' AND event = (SELECT id FROM nodes WHERE code = 'TST-SWISS-1123');
DELETE FROM edges WHERE kind = 'entered' AND dst = (SELECT id FROM nodes WHERE code = 'TST-SWISS-1123');
DELETE FROM nodes WHERE code = 'TST-SWISS-1123';
DELETE FROM nodes WHERE kind = 'player' AND id NOT IN (SELECT src FROM edges) AND id NOT IN (SELECT dst FROM edges);
