DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE import_batch LIKE 'IMP-TEST-%');
DELETE FROM nodes WHERE import_batch LIKE 'IMP-TEST-%';
