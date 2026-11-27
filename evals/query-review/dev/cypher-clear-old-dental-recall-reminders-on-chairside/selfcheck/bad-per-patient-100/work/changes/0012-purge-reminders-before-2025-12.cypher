// 0012: delete reminders sent before 2025-12-01 with their FOR/FROM/ABOUT (up to 4 entities each: 700 x 4 = 2,800 per transaction). Patients, practices and recalls stay.
MATCH (p:Patient)
CALL (p) { MATCH (r:Reminder)-[:FOR]->(p) WHERE r.sentAt < datetime('2025-12-01T00:00:00Z') DETACH DELETE r } IN TRANSACTIONS OF 100 ROWS;
