DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'track' AND import_batch LIKE 'IMP-TEST-%');
DELETE FROM nodes WHERE kind = 'track' AND import_batch LIKE 'IMP-TEST-%';
