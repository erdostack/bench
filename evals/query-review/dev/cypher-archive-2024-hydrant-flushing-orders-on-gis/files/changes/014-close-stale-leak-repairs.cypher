// ticket: OPS-3318
// what: cancel the repair orders raised by the 2025-09 leak-detection pilot that were never worked
// check: MATCH (w:WorkOrder {type: 'repair', status: 'open'}) WHERE w.woNo STARTS WITH 'LDP-' RETURN count(w);
MATCH (w:WorkOrder {type: 'repair', status: 'open'})
WHERE w.woNo STARTS WITH 'LDP-'
CALL {
  WITH w
  SET w.status = 'cancelled', w.closedAt = datetime('2025-10-01T00:00:00Z')
} IN TRANSACTIONS OF 2000 ROWS;
