WITH RECURSIVE needed(course_id) AS (
    SELECT requires_id FROM prerequisite
    WHERE course_id = :course_id AND kind = 'required'
    UNION
    SELECT p.requires_id
    FROM needed n
    JOIN prerequisite p ON p.course_id = n.course_id
    WHERE p.kind = 'required'
)
SELECT course_id FROM needed WHERE course_id <> :course_id;
