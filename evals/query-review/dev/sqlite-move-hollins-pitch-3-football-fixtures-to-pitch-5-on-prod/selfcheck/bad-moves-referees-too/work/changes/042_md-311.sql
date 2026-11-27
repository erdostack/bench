-- ticket: MD-311
UPDATE edges SET dst = (SELECT id FROM nodes WHERE code = 'HP-5')
WHERE kind = 'played_at' AND dst = (SELECT id FROM nodes WHERE code = 'HP-3')
  AND src IN (SELECT id FROM nodes WHERE kind = 'fixture' AND kickoff >= '2026-11-28');
DELETE FROM edges WHERE kind = 'refereed_by'
  AND src IN (SELECT src FROM edges WHERE kind = 'played_at' AND dst = (SELECT id FROM nodes WHERE code = 'HP-5'))
  AND src IN (SELECT id FROM nodes WHERE kickoff >= '2026-11-28');
