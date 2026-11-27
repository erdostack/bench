The rerun as written would double farms 251-300: that chunk committed, then the job_state write failed
("database is locked"), so job_state still says 250. I made the insert keyed on what an edge is
(farm, plant, kind 'ships_to', year): NOT EXISTS against edges with the year, so the 2024 edges don't stop
it and rows already written are skipped. Same 50-farm chunks (~150 rows per transaction), still returns the
edges written. Check: `SELECT src, dst, year, count(*) FROM edges WHERE kind='ships_to' GROUP BY 1,2,3
HAVING count(*) > 1` should return nothing after tonight's run.
