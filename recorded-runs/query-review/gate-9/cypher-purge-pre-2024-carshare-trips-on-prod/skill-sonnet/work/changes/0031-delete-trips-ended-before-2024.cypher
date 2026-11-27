// what: delete every Trip that ended before 2024-01-01T00:00:00Z, with its TOOK, USED, STARTED_IN and BILLED_ON relationships; Invoice, Member, Car and Zone nodes stay
// why: retention (docs/retention.md): trips are kept to the end of the second full calendar year after they ended; the trip history queries are slow with the old ones
// limit: a trip has at most 4 relationships, so at most 5 nodes and relationships; 1000 trips per transaction is at most 5000 (limit 10,000, docs/environment.md)
// count: MATCH (t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') RETURN count(t);   // docs say about 410,000; record the real number here before the run, expect 0 after
// check: MATCH (i:Invoice) RETURN count(i);   // same number before and after
// question for the reviewer: trips with no endedAt are not matched (null < date is null); confirm there are none that should go: MATCH (t:Trip) WHERE t.endedAt IS NULL RETURN count(t);
// not run: no copy of prod exists (docs/environment.md); to be reviewed in a PR and run by the fleet on-call with bin/tq prod --file changes/0031-delete-trips-ended-before-2024.cypher
// assumes Neo4j 5.26 (scope clause CALL (t) { } needs 5.23 or later); put EXPLAIN in front on prod first to confirm it compiles
// safe to re-run if it stops part-way: batches that committed stay deleted and it only matches trips still in scope
MATCH (t:Trip)
WHERE t.endedAt < datetime('2024-01-01T00:00:00Z')
CALL (t) { DETACH DELETE t } IN TRANSACTIONS OF 1000 ROWS;
