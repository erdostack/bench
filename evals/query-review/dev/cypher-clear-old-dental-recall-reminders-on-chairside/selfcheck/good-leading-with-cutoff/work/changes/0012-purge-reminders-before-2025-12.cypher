// 0012: delete reminders sent before 2025-12-01 with their FOR/FROM/ABOUT (up to 4 entities each: 700 x 4 = 2,800 per transaction). Patients, practices and recalls stay.
WITH datetime('2025-12-01T00:00:00Z') AS cutoff
MATCH (r:Reminder) WHERE r.sentAt < cutoff
CALL (r) { DETACH DELETE r } IN TRANSACTIONS OF 500 ROWS;
