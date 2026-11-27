-- Every course needed before :course_id, back through required and concurrent prerequisites.
-- recommended edges are never followed. UNION (not UNION ALL) on the course id ends the walk on cycles,
-- and the starting course is left out of the result.
WITH RECURSIVE chain (course_id) AS (
    SELECT p.requires_id
    FROM prerequisite p
    WHERE p.course_id = :course_id AND p.kind IN ('required', 'concurrent')
    UNION
    SELECT p.requires_id
    FROM chain c JOIN prerequisite p ON p.course_id = c.course_id
    WHERE p.kind IN ('required', 'concurrent')
)
SELECT course_id
FROM chain
WHERE course_id <> :course_id
ORDER BY course_id;
