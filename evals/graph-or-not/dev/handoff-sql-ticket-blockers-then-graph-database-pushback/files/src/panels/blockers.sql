-- Everything that blocks $1, directly or through other blockers, nearest first.
WITH RECURSIVE blockers (id, depth, path) AS (
    SELECT b.blocker_id, 1, ',' || b.ticket_id || ',' || b.blocker_id || ','
    FROM ticket_block b
    WHERE b.ticket_id = $1
    UNION ALL
    SELECT b.blocker_id, r.depth + 1, r.path || b.blocker_id || ','
    FROM blockers r
    JOIN ticket_block b ON b.ticket_id = r.id
    WHERE r.path NOT LIKE '%,' || b.blocker_id || ',%'
)
SELECT t.id, t.title, t.status, MIN(r.depth) AS depth
FROM blockers r
JOIN ticket t ON t.id = r.id
WHERE t.id <> $1
GROUP BY t.id, t.title, t.status
ORDER BY depth, t.id;
