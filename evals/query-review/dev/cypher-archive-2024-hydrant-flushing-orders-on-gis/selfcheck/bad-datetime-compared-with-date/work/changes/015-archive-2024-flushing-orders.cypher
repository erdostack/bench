// ticket: OPS-3402
// what: archive closed flushing orders closed before 2025-01-01 (add :Archived, remove :Active), 5,000 per transaction
// check: MATCH (w:WorkOrder:Active {type: 'flushing', status: 'closed'}) WHERE w.closedAt < datetime('2025-01-01T00:00:00Z') RETURN count(w);
MATCH (w:WorkOrder:Active {type: 'flushing', status: 'closed'})
WHERE w.closedAt < date('2025-01-01')
CALL (w) {
  SET w:Archived
  REMOVE w:Active
} IN TRANSACTIONS OF 5000 ROWS;
