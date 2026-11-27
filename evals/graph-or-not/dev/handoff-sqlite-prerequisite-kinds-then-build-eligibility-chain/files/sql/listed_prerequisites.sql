SELECT c.code, p.kind
FROM prerequisite p
JOIN course c ON c.id = p.requires_id
WHERE p.course_id = :course_id
ORDER BY c.code;
