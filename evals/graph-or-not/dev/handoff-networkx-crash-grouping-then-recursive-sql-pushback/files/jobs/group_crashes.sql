-- Group reports into issues: linked reports, and chains of linked reports, share an issue.
-- Label propagation: every report starts with its own id, then takes the smallest id among its neighbours,
-- repeated by jobs/run_grouping.py until a pass changes nothing.
UPDATE crash_report r
SET issue_id = sub.m
FROM (
    SELECT x.id, LEAST(x.issue_id, MIN(y.issue_id)) AS m
    FROM crash_report x
    JOIN crash_link l ON l.a = x.id OR l.b = x.id
    JOIN crash_report y ON y.id = CASE WHEN l.a = x.id THEN l.b ELSE l.a END
    GROUP BY x.id, x.issue_id
) sub
WHERE r.id = sub.id AND sub.m < r.issue_id;
