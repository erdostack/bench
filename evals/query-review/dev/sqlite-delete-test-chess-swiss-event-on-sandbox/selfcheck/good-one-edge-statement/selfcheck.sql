DELETE FROM edges WHERE (kind = 'paired' AND event IN (SELECT id FROM nodes WHERE kind = 'event' AND code = 'TST-SWISS-1123')) OR (kind = 'entered' AND dst IN (SELECT id FROM nodes WHERE kind = 'event' AND code = 'TST-SWISS-1123'));
DELETE FROM nodes WHERE kind = 'event' AND code = 'TST-SWISS-1123';
