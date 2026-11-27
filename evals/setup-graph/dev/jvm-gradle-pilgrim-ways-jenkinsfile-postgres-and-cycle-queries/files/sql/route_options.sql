-- Ways to walk from W001 to W020 in at most 60 km, shortest first.
WITH RECURSIVE edge AS (
  SELECT from_code AS a, to_code AS b, km FROM leg
  UNION ALL
  SELECT to_code, from_code, km FROM leg
), route (here, km) AS (
  SELECT 'W001'::text, 0::numeric
  UNION ALL
  SELECT e.b, r.km + e.km
  FROM route r JOIN edge e ON e.a = r.here
  WHERE r.km + e.km <= 60
) CYCLE here SET is_cycle USING path
SELECT path, km FROM route WHERE here = 'W020' AND NOT is_cycle ORDER BY km LIMIT 10;
