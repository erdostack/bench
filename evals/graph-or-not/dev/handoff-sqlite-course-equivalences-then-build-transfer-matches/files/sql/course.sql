SELECT c.code, c.title, c.credits, i.name
FROM course c JOIN institution i ON i.id = c.institution_id
WHERE c.id = :course_id;
