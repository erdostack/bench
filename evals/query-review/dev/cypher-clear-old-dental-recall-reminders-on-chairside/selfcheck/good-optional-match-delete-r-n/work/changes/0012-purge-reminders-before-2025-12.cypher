// 0012: delete reminders sent before 2025-12-01 with their FOR/FROM/ABOUT (up to 4 entities each: 700 x 4 = 2,800 per transaction). Patients, practices and recalls stay.
MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-12-01T00:00:00Z')
CALL (r) {
  OPTIONAL MATCH (r)-[x]-()
  DELETE x, r
} IN TRANSACTIONS OF 750 ROWS;
