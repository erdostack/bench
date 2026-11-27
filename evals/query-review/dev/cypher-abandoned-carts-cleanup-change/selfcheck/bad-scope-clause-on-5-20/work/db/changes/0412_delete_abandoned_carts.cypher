MATCH (c:Cart)
WHERE c.status = 'open' AND c.updatedAt < datetime('2026-08-25T00:00:00Z')
CALL (c) {
  DETACH DELETE c
} IN TRANSACTIONS OF 20000 ROWS;
