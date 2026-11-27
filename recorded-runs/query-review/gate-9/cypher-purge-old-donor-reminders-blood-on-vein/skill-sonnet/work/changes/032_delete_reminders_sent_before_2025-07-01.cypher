// 032 (DP-114): retention. Deletes every Reminder sent before 2025-07-01T00:00:00Z, whatever its channel or kind, with its
// TO and ABOUT relationships. Donors and appointments stay (docs/retention.md). About 236,000 reminders (docs/model.md).
// A reminder has at most 2 relationships, so 3 deletions a reminder; 3000 reminders a transaction is at most 9000 (limit 10,000).
// Count before (record the number here, then 0 after):
//   MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-07-01T00:00:00Z') RETURN count(r);
// Also the same before and after: MATCH (d:Donor) RETURN count(d);  MATCH (p:Appointment) RETURN count(p);
// Question for the reviewer: a reminder with no sentAt is not matched; check MATCH (r:Reminder) WHERE r.sentAt IS NULL RETURN count(r);
// Not run: no copy of the graph can be reached (docs/environments.md). Neo4j 5.26, the CALL (r) scope form needs 5.23 or later;
// put EXPLAIN in front on vein first. Safe to apply again if it stops part-way: it only matches reminders still in scope.
// Reviewed by: (pending). Applied by the donor-data on-call.
MATCH (r:Reminder)
WHERE r.sentAt < datetime('2025-07-01T00:00:00Z')
CALL (r) {
  DETACH DELETE r
} IN TRANSACTIONS OF 3000 ROWS;
