-- Courses equivalent to :course_id, with the fewest equivalence rows between them.
-- Registrar's rules: equivalence is transitive with no limit; approved and provisional rows count,
-- withdrawn ones never do; a pair is stored once in either order, so each row is read both ways.
-- Reading pairs both ways makes every pair a loop, so each walk carries the courses it has visited.
WITH RECURSIVE
pair (a, b) AS (
    SELECT course_a, course_b FROM course_equivalence WHERE status = 'approved'
    UNION ALL
    SELECT course_b, course_a FROM course_equivalence WHERE status = 'approved'
),
walk (course_id, links, visited) AS (
    SELECT :course_id, 0, ',' || :course_id || ','
    UNION ALL
    SELECT p.b, w.links + 1, w.visited || p.b || ','
    FROM walk w
    JOIN pair p ON p.a = w.course_id
    WHERE instr(w.visited, ',' || p.b || ',') = 0
)
SELECT course_id, MIN(links) AS links
FROM walk
WHERE course_id <> :course_id
GROUP BY course_id;
