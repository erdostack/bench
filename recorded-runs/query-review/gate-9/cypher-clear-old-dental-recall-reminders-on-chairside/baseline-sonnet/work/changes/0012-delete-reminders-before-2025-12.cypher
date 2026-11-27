// 0012: delete reminders sent before 2025-12-01 (about 6.3 million) because the reminders list in the surgery screens is slow to load. Patients, practices and recalls are kept; only Reminder nodes and their FOR/FROM/ABOUT relationships go.
// Count before and after (after should be 0): MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-12-01T00:00:00Z') RETURN count(r);
// Batching: a reminder is 1 node + 2 or 3 relationships = at most 4 entities, and a transaction may delete at most 3,000 entities (docs/environments.md), so 700 reminders = at most 2,800 per transaction (about 9,000 transactions).
MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-12-01T00:00:00Z')
CALL (r) {
  DETACH DELETE r
} IN TRANSACTIONS OF 700 ROWS;
