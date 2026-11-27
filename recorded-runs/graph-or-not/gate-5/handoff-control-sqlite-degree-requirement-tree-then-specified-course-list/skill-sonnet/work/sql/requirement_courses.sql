WITH RECURSIVE sub(id) AS (
    SELECT id FROM requirement WHERE id = :requirement_id
    UNION
    SELECT r.id FROM requirement r JOIN sub s ON r.parent_id = s.id
)
SELECT DISTINCT course_code FROM requirement_course WHERE requirement_id IN (SELECT id FROM sub) ORDER BY course_code;
