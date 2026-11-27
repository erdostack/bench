WITH RECURSIVE walk(id, metres, lifts, trail) AS (
  SELECT $from, 0.0, 0, '/' || $from || '/'
  UNION ALL
  SELECT s.to_id, w.metres + s.metres, w.lifts + (j.kind = 'lift'), w.trail || s.to_id || '/'
  FROM walk w JOIN segment s ON s.from_id = w.id JOIN junction j ON j.id = s.to_id
  WHERE instr(w.trail, '/' || s.to_id || '/') = 0 AND w.metres < 2000
)
SELECT metres, lifts, trail FROM walk WHERE id = $to ORDER BY metres LIMIT 1;
