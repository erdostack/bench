-- Every course that must be passed, directly or indirectly, before MATH-340.
WITH RECURSIVE chain(code, depth) AS (
  SELECT needs, 1 FROM prerequisite WHERE course = 'MATH-340'
  UNION
  SELECT p.needs, c.depth + 1
  FROM chain AS c JOIN prerequisite AS p ON p.course = c.code
  WHERE c.depth < 12
)
SELECT c.code, co.title, MIN(c.depth) AS steps_away
FROM chain AS c JOIN course AS co USING (code)
GROUP BY c.code, co.title
ORDER BY steps_away, c.code;
