// ticket: FLEET-??? clear WAITLISTED places with since before 2026-05-01 (lapsed, never renewed). Ticket id needed from requester. Question for reviewer: cutoff is the requested 2026-05-01; the six-month lapse rule in docs/model.md would put it at 2026-05-26 today, so places from 1-25 May are kept. OK? Assumes Cypher 5 on Neo4j 5.24 (scope clause CALL (w) needs 5.23+); run with bin/cq fleet --file, so it is auto-commit, as IN TRANSACTIONS requires.
// Before: MATCH (:Member)-[w:WAITLISTED]->(:Zone) WHERE w.since < date('2026-05-01') RETURN count(w) AS to_delete;   (record N in the PR; not yet counted, nothing could be run here)
// After:  the same query must return 0; MATCH ()-[w:WAITLISTED]->() RETURN count(w) must equal 33,000-ish minus N.
MATCH (:Member)-[w:WAITLISTED]->(:Zone)
WHERE w.since < date('2026-05-01')
CALL (w) {
  DELETE w
} IN TRANSACTIONS OF 5000 ROWS;
