// 032 (DP-114): retention review, reminders sent before 2025-07-01 00:00 UTC are deleted, whatever the channel or kind.
// Deletes those Reminder nodes with their TO and ABOUT relationships, about 236,000 nodes. Donors and Appointments stay.
// A reminder is 1 node + at most 2 relationships = 3, so 2000 per transaction is at most 6,000 objects, under the 10,000 limit.
// Safe to apply again: it only matches reminders still there.
// Count before and after (about 236,000 before, 0 after):
//   MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-07-01T00:00:00Z') RETURN count(r);
// Donors and appointments must not change: MATCH (d:Donor) RETURN count(d); MATCH (a:Appointment) RETURN count(a);
// Not yet applied. Needs review in a pull request, then the donor-data on-call applies it.
MATCH (r:Reminder)
WHERE r.sentAt < datetime('2025-07-01T00:00:00Z')
CALL (r) {
  DETACH DELETE r
} IN TRANSACTIONS OF 2000 ROWS;
