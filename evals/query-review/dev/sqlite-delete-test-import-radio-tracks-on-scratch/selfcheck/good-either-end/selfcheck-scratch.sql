CREATE TEMP TABLE junk AS SELECT id FROM nodes WHERE import_batch = 'IMP-TEST-1121' AND kind = 'track';
DELETE FROM edges WHERE src IN (SELECT id FROM junk) OR dst IN (SELECT id FROM junk);
DELETE FROM nodes WHERE id IN (SELECT id FROM junk);
