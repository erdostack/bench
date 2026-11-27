-- every door reachable from the library's main door without steps, with the shortest distance found
WITH RECURSIVE reach(id, metres, trail) AS (
  SELECT 'D-LIB-1', 0.0, '/D-LIB-1/'
  UNION ALL
  SELECT s.to_id, r.metres + s.metres, r.trail || s.to_id || '/'
  FROM reach r JOIN segment s ON s.from_id = r.id
  WHERE s.step_free = 1 AND instr(r.trail, '/' || s.to_id || '/') = 0 AND r.metres < 1500
)
SELECT j.id, j.building, min(r.metres) AS metres
FROM reach r JOIN junction j ON j.id = r.id
WHERE j.kind = 'door'
GROUP BY j.id
ORDER BY metres;
