// ticket: HOL-58 purge lapsed seat holds created before 2026-10-01, except holds with a depositRef (accounts reconcile the deposit refund against the hold, docs/holds.md). Deletes HOLDS relationships only; 10,000 per transaction (limit 25,000, docs/environments.md). Cypher 5, Neo4j 5.26 (CALL (h) needs 5.23+). Question for the reviewer: the ticket's statement has no depositRef filter and no batching; this file adds both.
MATCH (:Customer)-[h:HOLDS]->(:Departure)
WHERE h.status = 'lapsed' AND h.createdAt < datetime('2026-10-01T00:00:00Z') AND h.depositRef IS NULL
CALL (h) {
  DELETE h
} IN TRANSACTIONS OF 10000 ROWS;
