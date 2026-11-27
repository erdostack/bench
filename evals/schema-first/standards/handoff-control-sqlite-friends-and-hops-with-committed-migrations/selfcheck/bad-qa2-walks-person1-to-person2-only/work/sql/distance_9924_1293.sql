WITH RECURSIVE f(x, d) AS (
  SELECT 9924, 0
  UNION
  SELECT k.person2Id, f.d + 1 FROM f JOIN knows k ON k.person1Id = f.x WHERE f.d < 20
)
SELECT d FROM (SELECT d FROM f WHERE x = 1293 UNION ALL SELECT -1) ORDER BY d = -1, d LIMIT 1;
