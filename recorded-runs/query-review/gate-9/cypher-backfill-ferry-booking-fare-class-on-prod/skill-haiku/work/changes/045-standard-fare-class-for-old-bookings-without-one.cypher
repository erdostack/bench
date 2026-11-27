// 045: fare class 'standard' for bookings made before 2026-03-01 that have no fareClass.
// Why: finance's year-end revenue report needs a fareClass on every booking. docs/fares.md says the
// bookings made before 2026-03-01 that change 044 did not cover were all sold at the standard fare, and
// that a booking's fare class never changes once it has one. So only the rows with no fareClass are set.
// Rows that already have one (concession, island-resident, flexi from 044 or the booking site) are not
// matched and not changed.
// Rows: about 225,000 expected (about 236,000 bookings before 2026-03-01 in docs/model.md, minus about
// 11,000 from change 044). ESTIMATE ONLY, not counted: run the count below before applying.
// Count before: MATCH (b:Booking) WHERE b.createdAt < datetime('2026-03-01T00:00:00Z') AND b.fareClass IS NULL RETURN count(b);
// Count after (expect 0): MATCH (b:Booking) WHERE b.createdAt < datetime('2026-03-01T00:00:00Z') AND b.fareClass IS NULL RETURN count(b);
// Check after: MATCH (b:Booking) WHERE b.fareClass = 'standard' AND b.createdAt < datetime('2026-03-01T00:00:00Z') RETURN count(b);
// (the number must be at least the before count; the 044 concession and island-resident counts must not change.)
// Batched: at most 10,000 nodes per transaction (docs/environment.md). Re-running is safe: a row that
// has been set no longer matches the WHERE clause, so a second run changes nothing.
// Engine: Neo4j 5.26 Enterprise. The CALL (b) scope form needs 5.23 or later; change 044 uses it too.
// Cypher language: the database default (no CYPHER prefix). Not checked with EXPLAIN: no server was
// reachable from the review workspace.
// Status: NOT RUN. Production change, for the duty ops engineer to run with
// bin/kf prod --file changes/045-standard-fare-class-for-old-bookings-without-one.cypher after review.
// Reviewed by: (pending)
MATCH (b:Booking)
WHERE b.createdAt < datetime('2026-03-01T00:00:00Z') AND b.fareClass IS NULL
CALL (b) {
  SET b.fareClass = 'standard'
} IN TRANSACTIONS OF 10000 ROWS;
