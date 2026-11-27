// what: delete the trips that ended before 2024-01-01T00:00:00Z, with their TOOK, USED, STARTED_IN and BILLED_ON relationships; invoices, members, cars and zones stay
// why: retention (docs/retention.md): a trip record is kept until the end of the second full calendar year after it ended, so these are past that; the trip history queries are slow on this volume
// count before: MATCH (t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') RETURN count(t);   (docs/model.md says about 410,000)
// count before (relationships): MATCH (t:Trip)-[r]-() WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') RETURN count(r);
// count after: both counts above should return 0; the invoice count must not change
// per transaction: a trip has at most four relationships, so 1000 trips is at most 5,000 nodes and relationships, within the 10,000 limit (docs/environment.md)
// runs as an implicit (auto-commit) transaction, as bin/tq sends it; re-running acts only on trips still in scope
MATCH (t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z')
CALL (t) { DETACH DELETE t } IN TRANSACTIONS OF 1000 ROWS;
