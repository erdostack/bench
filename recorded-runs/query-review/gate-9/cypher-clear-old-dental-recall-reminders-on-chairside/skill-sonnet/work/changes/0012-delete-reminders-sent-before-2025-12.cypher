// 0012: delete reminders sent before 2025-12-01 (about 6.3 million of 9.1 million), with their FOR / FROM / ABOUT relationships, because the surgery screens' reminders list is slow to load. Patients, practices and recalls are kept (docs/graph.md). Count before and after: MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-12-01T00:00:00Z') RETURN count(r); (after must be 0; also check MATCH (r:Reminder) RETURN count(r) fell by the before count, and that patient, practice and recall counts are unchanged). Batches of 700 reminders: each reminder is 1 node plus 2 or 3 relationships (4 entities at most), so a batch deletes at most 2,800 entities, under the 3,000 limit in docs/environments.md. Questions for the reviewer: not run anywhere, as chairside is the only graph; please confirm with EXPLAIN that the Reminder(sentAt) index is used and that the runner sends the file as an auto-commit statement (IN TRANSACTIONS fails inside an explicit transaction). Run out of hours.
MATCH (r:Reminder)
WHERE r.sentAt < datetime('2025-12-01T00:00:00Z')
CALL (r) {
  DETACH DELETE r
} IN TRANSACTIONS OF 700 ROWS;
