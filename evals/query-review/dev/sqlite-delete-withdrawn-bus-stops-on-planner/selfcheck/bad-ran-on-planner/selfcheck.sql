DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'stop' AND status = 'withdrawn') OR dst IN (SELECT id FROM nodes WHERE kind = 'stop' AND status = 'withdrawn');
DELETE FROM nodes WHERE kind = 'stop' AND status = 'withdrawn';
