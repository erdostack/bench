// One-off backfill, 2026-11-16: 96 million WORKS_AT.
MATCH (p:Person)-[w:WORKS_AT]->(c:Company)
CALL (p, w, c) {
  MERGE (p)-[e:EMPLOYED_BY]->(c)
  ON CREATE SET e.since = w.since, e.title = w.title, e.copiedAt = datetime()
} IN TRANSACTIONS OF 20000 ROWS;
