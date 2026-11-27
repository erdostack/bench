// ticket: OPS-3402
// what: archive flushing orders closed in 2024 or earlier
// check: MATCH (w:WorkOrder:Active {type: 'flushing', status: 'closed'}) WHERE w.closedAt.year <= 2024 RETURN count(w);
MATCH (w:WorkOrder {type: 'flushing', status: 'closed'})
WHERE w.closedAt.year <= 2024 AND w:Active
CALL {
  WITH w
  SET w:Archived
} IN TRANSACTIONS OF 2000 ROWS;

MATCH (w:WorkOrder:Archived:Active)
CALL {
  WITH w
  REMOVE w:Active
} IN TRANSACTIONS OF 2000 ROWS;
