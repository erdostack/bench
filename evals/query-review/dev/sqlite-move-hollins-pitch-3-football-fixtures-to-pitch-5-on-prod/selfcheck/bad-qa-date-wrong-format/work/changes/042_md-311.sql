-- ticket: MD-311: HP-3 fixtures from 28/11/2026 move to HP-5
UPDATE edges SET dst = (SELECT id FROM nodes WHERE code = 'HP-5')
WHERE kind = 'played_at' AND dst = (SELECT id FROM nodes WHERE code = 'HP-3')
  AND src IN (SELECT id FROM nodes WHERE kind = 'fixture' AND kickoff >= '28/11/2026');
