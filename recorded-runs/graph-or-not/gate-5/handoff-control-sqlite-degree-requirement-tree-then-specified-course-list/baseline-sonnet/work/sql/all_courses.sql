-- Every course that counts toward :requirement_id, sub-requirements at any depth included, each course once.
WITH RECURSIVE sub(id) AS (
    SELECT id FROM requirement WHERE id = :requirement_id
    UNION
    SELECT r.id FROM requirement r JOIN sub s ON r.parent_id = s.id
)
SELECT DISTINCT rc.course_code
FROM requirement_course rc
WHERE rc.requirement_id IN (SELECT id FROM sub)
ORDER BY rc.course_code;
