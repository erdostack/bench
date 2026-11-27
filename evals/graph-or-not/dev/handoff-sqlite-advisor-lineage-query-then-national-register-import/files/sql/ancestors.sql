-- Academic ancestors of :researcher_id, with the generation at which each first appears.
-- Stops at 30 generations and carries the path, so a data-entry loop cannot run forever.
WITH RECURSIVE up(id, generation, path) AS (
    SELECT advisor_id, 1, ',' || :researcher_id || ',' || advisor_id || ','
    FROM advising WHERE student_id = :researcher_id
    UNION ALL
    SELECT a.advisor_id, up.generation + 1, up.path || a.advisor_id || ','
    FROM up
    JOIN advising a ON a.student_id = up.id
    WHERE up.generation < 30 AND instr(up.path, ',' || a.advisor_id || ',') = 0
)
SELECT r.id, r.name, MIN(up.generation) AS generation
FROM up JOIN researcher r ON r.id = up.id
GROUP BY r.id, r.name
ORDER BY generation, r.name;
