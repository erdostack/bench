MATCH (f:Fan)-[m:MEMBER_OF]->(:SupportersClub)
WHERE f.lastSeen < datetime('2025-01-01T00:00:00Z')
CALL (m) { DELETE m } IN TRANSACTIONS OF 10000 ROWS;
