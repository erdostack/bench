-- Everything needed before taking :course_id: required and concurrent prerequisites, followed all the way
-- back. Recommended rows are never followed, so nothing reached only through one appears.
-- UNION on requires_id alone (no depth or path column) is what ends the walk on the cross-listed loops.
WITH RECURSIVE needed(course_id) AS (
    SELECT :course_id
    UNION
    SELECT p.requires_id
    FROM prerequisite p
    JOIN needed n ON p.course_id = n.course_id
    WHERE p.kind IN ('required', 'concurrent')
)
SELECT c.code, c.title, c.level
FROM needed n
JOIN course c ON c.id = n.course_id
WHERE n.course_id <> :course_id
ORDER BY c.level, c.code;
