WITH RECURSIVE below(id, depth) AS (
    SELECT id, 0 FROM requirement WHERE id = :requirement_id
    UNION ALL
    SELECT r.id, b.depth + 1 FROM requirement r JOIN below b ON r.parent_id = b.id
)
SELECT rc.course_code
FROM requirement_course rc
WHERE rc.requirement_id IN (SELECT id FROM below)
GROUP BY rc.course_code
ORDER BY rc.course_code;
