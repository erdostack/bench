WITH RECURSIVE needed(course_id, depth) AS (
    SELECT requires_id, 1 FROM prerequisite
    WHERE course_id = :course_id AND kind IN ('required', 'concurrent')
    UNION
    SELECT p.requires_id, n.depth + 1
    FROM needed n
    JOIN prerequisite p ON p.course_id = n.course_id
    WHERE p.kind IN ('required', 'concurrent')
)
SELECT DISTINCT course_id FROM needed WHERE course_id <> :course_id;
