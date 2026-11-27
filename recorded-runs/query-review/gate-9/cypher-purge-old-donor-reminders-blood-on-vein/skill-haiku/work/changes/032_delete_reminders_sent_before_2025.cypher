// 032 (DP-114): retention. Reminders sent before 2025-07-01 00:00 UTC are deleted, whatever the channel or kind
// (docs/retention.md). The donor and the appointment a reminder points at stay.
// A reminder has at most two relationships (TO and ABOUT), so 1000 reminders is at most 3000 nodes and
// relationships in a batch, under the 10,000 limit (docs/changes.md).
// Count before (about 236,000 per docs/model.md):
//   MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-07-01T00:00:00Z') RETURN count(r);
// Count of reminders with no sentAt (must not change; they were not sent):
//   MATCH (r:Reminder) WHERE r.sentAt IS NULL RETURN count(r);
// Count after: the first count above should return 0; the second count and the Donor and Appointment counts must not change.
MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-07-01T00:00:00Z')
CALL (r) {
  DETACH DELETE r
} IN TRANSACTIONS OF 1000 ROWS;
