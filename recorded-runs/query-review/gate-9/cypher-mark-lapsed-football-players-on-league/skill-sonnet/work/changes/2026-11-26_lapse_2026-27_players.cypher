// 2026-27 window closed 2026-10-31: lapse players not registered for 2026-27 (docs/registration.md). Players only; coaches are not part of this.
// About 3,900 players (count 2026-11-25), so it is batched: 500 nodes per transaction, limit 1,000 (docs/operations.md). Cypher 5 on Neo4j 5.24; CALL (p) needs 5.23+.
// Question for reviewer: bin/reg runs auto-commit, which CALL ... IN TRANSACTIONS needs; please confirm when you run it. Re-running is safe: lapsed players no longer match.
MATCH (p:Player:Registered)
WHERE p.lastSeason < '2026-27'
CALL (p) {
  SET p:Lapsed
  REMOVE p:Registered
} IN TRANSACTIONS OF 500 ROWS;
