// what: delete Trip nodes that ended before 2024-01-01T00:00:00Z, with their relationships (TOOK, USED, STARTED_IN, BILLED_ON); Invoices, Members, Cars and Zones stay
// why: retention (docs/retention.md): trips are kept to the end of the second full calendar year after they ended; trip history queries are slow
// batching: a trip is 1 node + at most 4 relationships = 5 deleted, so 1000 trips per transaction is at most 5,000, under the 10,000 cap. Re-running carries on from where it stopped.
// count before: MATCH (t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') RETURN count(t);   // expect about 410,000
// count after:  same query, expect 0
// check invoices untouched: MATCH (i:Invoice) RETURN count(i);   // same before and after
// not yet run. Needs review in a PR, then the fleet on-call runs: bin/tq prod --file changes/0031-delete-trips-ended-before-2024.cypher
MATCH (t:Trip)
WHERE t.endedAt < datetime('2024-01-01T00:00:00Z')
CALL (t) { DETACH DELETE t } IN TRANSACTIONS OF 1000 ROWS;
