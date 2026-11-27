WITH RECURSIVE walk(course_id, path) AS (
    SELECT requires_id, ',' || :course_id || ',' || requires_id || ','
    FROM prerequisite WHERE course_id = :course_id AND kind <> 'recommended'
    UNION ALL
    SELECT p.requires_id, w.path || p.requires_id || ','
    FROM walk w
    JOIN prerequisite p ON p.course_id = w.course_id
    WHERE p.kind <> 'recommended' AND instr(w.path, ',' || p.requires_id || ',') = 0
)
SELECT DISTINCT course_id FROM walk;
