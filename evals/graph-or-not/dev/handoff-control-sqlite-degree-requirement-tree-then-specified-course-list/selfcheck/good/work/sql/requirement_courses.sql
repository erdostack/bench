-- Courses that count toward :requirement_id: listed under it or under any requirement nested inside it.
WITH RECURSIVE below(id) AS (
    SELECT :requirement_id
    UNION ALL
    SELECT r.id FROM requirement r JOIN below b ON r.parent_id = b.id
)
SELECT DISTINCT rc.course_code
FROM requirement_course rc JOIN below b ON rc.requirement_id = b.id;
