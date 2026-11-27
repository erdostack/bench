// 0014 (LK-2290): delete acoustic logger hits from before 2026, 20,000 per transaction.
// Check: MATCH ()-[h:HEARD]->() WHERE h.at < datetime('2026-01-01T00:00:00Z') RETURN count(h);
MATCH (:Logger)-[h:HEARD]->(:Main)
WHERE h.at < datetime('2026-01-01T00:00:00Z')
CALL {
  WITH h
  DELETE h
} IN TRANSACTIONS OF 20000 ROWS;
