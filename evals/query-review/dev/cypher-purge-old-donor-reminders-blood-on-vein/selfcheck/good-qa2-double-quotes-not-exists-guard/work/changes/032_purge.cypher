MATCH (r:Reminder)-[x]-() WHERE r.sentAt < datetime("2025-07-01T00:00:00Z")
CALL (x) { DELETE x } IN TRANSACTIONS OF 5000 ROWS;
MATCH (r:Reminder) WHERE r.sentAt < datetime("2025-07-01T00:00:00Z") AND NOT EXISTS { (r)--() }
CALL (r) { DELETE r } IN TRANSACTIONS OF 5000 ROWS;
