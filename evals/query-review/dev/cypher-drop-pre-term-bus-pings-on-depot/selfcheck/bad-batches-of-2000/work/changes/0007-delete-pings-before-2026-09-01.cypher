// 0007: delete pings before 2026-09-01, same batch size as 0006
MATCH (p:Ping)
WHERE p.at < datetime('2026-09-01T00:00:00Z')
CALL (p) {
  DETACH DELETE p
} IN TRANSACTIONS OF 2000 ROWS;
