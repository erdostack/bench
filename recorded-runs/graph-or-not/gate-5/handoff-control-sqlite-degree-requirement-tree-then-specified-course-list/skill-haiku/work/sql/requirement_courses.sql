WITH RECURSIVE subtree (id) AS (
    SELECT :requirement_id
    UNION
    SELECT r.id FROM requirement AS r JOIN subtree AS s ON r.parent_id = s.id
)
SELECT DISTINCT rc.course_code
FROM requirement_course AS rc JOIN subtree AS s ON rc.requirement_id = s.id
ORDER BY rc.course_code;
