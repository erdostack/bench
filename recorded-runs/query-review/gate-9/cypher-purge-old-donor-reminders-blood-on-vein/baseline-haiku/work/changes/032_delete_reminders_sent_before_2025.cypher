// 032 (DP-114): retention review. Reminders sent before 2025-07-01 00:00 UTC are deleted, whatever the channel or kind
// (docs/retention.md). Each reminder's TO and ABOUT relationships go with it. Donors and appointments stay.
// Should touch about 236,000 Reminder nodes and at most two relationships each.
// Count before and after (0 after):
//   MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-07-01T00:00:00Z') RETURN count(r);
// Batches of 2,000 reminders: at most 3 changes each (node, TO, ABOUT), so 6,000 per transaction, under the 10,000 limit in docs/changes.md.
// Not run: awaiting review and a run by the donor-data on-call with bin/vq vein --file changes/032_delete_reminders_sent_before_2025.cypher
MATCH (r:Reminder)
WHERE r.sentAt < datetime('2025-07-01T00:00:00Z')
CALL (r) {
  DETACH DELETE r
} IN TRANSACTIONS OF 2000 ROWS;
