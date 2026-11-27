// 045: set fareClass = 'standard' on bookings made before 2026-03-01 that still have no fare class.
// Why: finance needs a fare class on every booking for the year-end revenue report. Change 044 gave a class
// to the old concession / island-resident bookings and left the rest without one; docs/fares.md says every
// one of those was sold at the standard fare. Bookings that already have a fareClass are not touched
// (docs/fares.md: once a booking has one, nothing changes it), so the filter is `fareClass IS NULL`.
// How many: roughly 236,000 old bookings minus the roughly 11,000 from 044, about 225,000 nodes, in batches
// of 10,000 (limit in docs/environment.md). NOT YET COUNTED: the counts below are the reviewer's/ops check.
// Count before (rows this change will set; record it): MATCH (b:Booking) WHERE b.fareClass IS NULL AND b.createdAt < datetime('2026-03-01T00:00:00Z') RETURN count(b);
// Count after (must be 0):                              MATCH (b:Booking) WHERE b.fareClass IS NULL AND b.createdAt < datetime('2026-03-01T00:00:00Z') RETURN count(b);
// Also after: the 044 count (concession / island-resident, made before 2026-03-01) must equal its value before.
// Re-run is safe: a second run matches nothing, because the rows it set no longer have a null fareClass.
// Question for the reviewer: prod has no copy to try this on; please confirm the CALL (b) { ... } scope form
// with EXPLAIN (Neo4j 5.26 supports it from 5.23) and that the runner sends it as an auto-commit statement.
// Language assumed: Cypher 5 on Neo4j 5.26. Run by the duty ops engineer: bin/kf prod --file changes/045-standard-fare-class-for-remaining-old-bookings.cypher
MATCH (b:Booking)
WHERE b.fareClass IS NULL AND b.createdAt < datetime('2026-03-01T00:00:00Z')
CALL (b) {
  SET b.fareClass = 'standard'
} IN TRANSACTIONS OF 10000 ROWS;
