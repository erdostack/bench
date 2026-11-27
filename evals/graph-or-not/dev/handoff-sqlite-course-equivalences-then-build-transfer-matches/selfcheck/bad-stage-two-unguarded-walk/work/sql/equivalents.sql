WITH RECURSIVE reach(course_id, links) AS (
    SELECT :course_id, 0
    UNION
    SELECT CASE WHEN e.course_a = r.course_id THEN e.course_b ELSE e.course_a END, r.links + 1
    FROM reach r
    JOIN course_equivalence e ON r.course_id IN (e.course_a, e.course_b)
    WHERE e.status IN ('approved', 'provisional')
)
SELECT course_id, MIN(links) FROM reach WHERE course_id <> :course_id GROUP BY course_id;
