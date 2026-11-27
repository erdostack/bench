-- loops of at most 12 km that start and end at the Pine Flat trailhead
WITH RECURSIVE walk(at, km, trail, done) AS (
  SELECT 'J-0001', 0.0, '/J-0001/', 0
  UNION ALL
  SELECT s.to_junction, w.km + s.km, w.trail || s.to_junction || '/', s.to_junction = 'J-0001'
  FROM walk w JOIN segment s ON s.from_junction = w.at
  WHERE w.done = 0 AND w.km + s.km <= 12
    AND (instr(w.trail, '/' || s.to_junction || '/') = 0 OR (s.to_junction = 'J-0001' AND length(w.trail) > 15))
)
SELECT km, trail FROM walk WHERE done = 1 ORDER BY km LIMIT 20;
