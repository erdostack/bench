// ticket: OPS-3402
// what: archive closed flushing orders before 2025
// check: count(w) before and after
MATCH (w:WorkOrder:Active {type: 'flushing', status: 'closed'})
WHERE w.closedAt < datetime('2025-01-01T00:00:00Z')
SET w:Archived
REMOVE w:Active;
