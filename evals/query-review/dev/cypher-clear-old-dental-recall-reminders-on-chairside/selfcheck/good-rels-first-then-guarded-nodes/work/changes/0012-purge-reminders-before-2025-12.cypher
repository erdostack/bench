// 0012: delete reminders sent before 2025-12-01 with their FOR/FROM/ABOUT (up to 4 entities each: 700 x 4 = 2,800 per transaction). Patients, practices and recalls stay.
MATCH (r:Reminder)-[x:FOR|FROM|ABOUT]->() WHERE r.sentAt < datetime('2025-12-01T00:00:00Z')
CALL (x) { DELETE x } IN TRANSACTIONS OF 3000 ROWS;
MATCH (r:Reminder) WHERE r.sentAt < datetime('2025-12-01T00:00:00Z') AND NOT (r)--()
CALL (r) { DELETE r } IN TRANSACTIONS OF 3000 ROWS;
