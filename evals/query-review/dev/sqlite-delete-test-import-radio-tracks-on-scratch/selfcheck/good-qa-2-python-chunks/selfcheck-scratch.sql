DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind='track' AND import_batch='IMP-TEST-1121') OR dst IN (SELECT id FROM nodes WHERE kind='track' AND import_batch='IMP-TEST-1121');
DELETE FROM nodes WHERE id IN (SELECT id FROM nodes WHERE kind='track' AND import_batch='IMP-TEST-1121' LIMIT 200);
DELETE FROM nodes WHERE kind='track' AND import_batch='IMP-TEST-1121';
