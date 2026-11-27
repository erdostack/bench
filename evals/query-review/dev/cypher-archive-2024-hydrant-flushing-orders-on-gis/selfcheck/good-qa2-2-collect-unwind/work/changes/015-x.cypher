// ticket: OPS-3402
// archive closed flushing orders closed before 2025-01-01; count: MATCH (w:WorkOrder:Active {type: 'flushing', status: 'closed'}) WHERE w.closedAt < datetime('2025-01-01T00:00:00Z') RETURN count(w);
MATCH (w:WorkOrder:Active {type: 'flushing', status: 'closed'}) WHERE w.closedAt < datetime('2025-01-01T00:00:00Z')
WITH collect(w) AS ws UNWIND ws AS x
CALL (x) { SET x:Archived REMOVE x:Active } IN TRANSACTIONS OF 5000 ROWS;
