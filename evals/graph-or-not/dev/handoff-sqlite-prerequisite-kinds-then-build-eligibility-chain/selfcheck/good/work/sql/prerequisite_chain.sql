-- Everything a student needs before taking :course_id (registrar's rule, docs/graph/DECISION.md):
-- follow required and concurrent prerequisites all the way back; recommended ones never count, and nothing
-- reached only through a recommended one. UNION on the course id alone, so the cross-listed loops end.
WITH RECURSIVE needed(course_id) AS (
    SELECT requires_id FROM prerequisite
    WHERE course_id = :course_id AND kind IN ('required', 'concurrent')
    UNION
    SELECT p.requires_id
    FROM needed n
    JOIN prerequisite p ON p.course_id = n.course_id
    WHERE p.kind IN ('required', 'concurrent')
)
SELECT course_id FROM needed WHERE course_id <> :course_id;
