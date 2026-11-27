-- Round walks back to W001 of 15 to 40 km.
WITH RECURSIVE edge AS (
  SELECT from_code AS a, to_code AS b, km FROM leg
  UNION ALL
  SELECT to_code, from_code, km FROM leg
), walk (here, km) AS (
  SELECT 'W001'::text, 0::numeric
  UNION ALL
  SELECT e.b, w.km + e.km
  FROM walk w JOIN edge e ON e.a = w.here
  WHERE w.km + e.km <= 40
) CYCLE here SET closed USING path
SELECT path, km FROM walk WHERE closed AND here = 'W001' AND km >= 15 ORDER BY km LIMIT 10;
