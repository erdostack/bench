SELECT DISTINCT rc.course_code
FROM requirement_course rc
WHERE rc.requirement_id = :requirement_id
   OR rc.requirement_id IN (SELECT id FROM requirement WHERE parent_id = :requirement_id);
