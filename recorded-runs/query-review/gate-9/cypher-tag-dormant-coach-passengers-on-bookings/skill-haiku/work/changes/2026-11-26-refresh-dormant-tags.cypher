// What: bring the :Dormant label up to date for the Friday mailing export (docs/mailing.md).
// Dormant = a past passenger whose last tour ended before 2024-01-01, so it has lastTravelled before
// 2024-01-01. A passenger with no lastTravelled is an enquirer (docs/mailing.md, docs/model.md) and must
// never be :Dormant. Step 1 adds the label to passengers who qualify. Step 2 removes it from passengers
// who are labelled but no longer qualify: they have travelled since, or they have never travelled.
// Scope: :Passenger only. Passenger properties are not changed. :Enquirer is not changed.
// Counts before (run both, and keep them for the after comparison):
//   MATCH (p:Passenger) WHERE p.lastTravelled IS NOT NULL AND p.lastTravelled < date('2024-01-01') AND NOT p:Dormant RETURN count(p);
//   MATCH (p:Passenger:Dormant) WHERE p.lastTravelled IS NULL OR p.lastTravelled >= date('2024-01-01') RETURN count(p);
//   MATCH (p:Passenger) WHERE p.lastTravelled IS NULL AND p:Dormant RETURN count(p);   // enquirers wrongly tagged
// Expected: step 1 touches the first count (about 71,000 passengers last travelled before 2024, less any
// already labelled). Step 2 touches the second count. The third count must be 0 after both steps.
// After (must be 0): MATCH (p:Passenger) WHERE p:Dormant AND (p.lastTravelled IS NULL OR p.lastTravelled >= date('2024-01-01')) RETURN count(p);
// Batched: at most 10,000 rows per transaction (docs/where-it-runs.md). Re-running is safe: each step
// matches only rows that are not yet in the target state.
// Engine: Neo4j 5.24 Community. The CALL (p) scope form needs 5.23 or later. APOC is not installed.
// Cypher language: the database default (no CYPHER prefix).
// Status: NOT RUN. Production change. The systems lead runs it after review with
// bin/pg bookings --file changes/2026-11-26-refresh-dormant-tags.cypher
// Not checked with EXPLAIN and not counted: no copy of the database is reachable from the review workspace.
// Reviewed by: (pending)

// Step 1: label passengers who qualify and are not yet labelled.
MATCH (p:Passenger)
WHERE p.lastTravelled IS NOT NULL AND p.lastTravelled < date('2024-01-01') AND NOT p:Dormant
CALL (p) { SET p:Dormant } IN TRANSACTIONS OF 10000 ROWS;

// Step 2: remove the label from passengers who are labelled but do not qualify.
MATCH (p:Passenger:Dormant)
WHERE p.lastTravelled IS NULL OR p.lastTravelled >= date('2024-01-01')
CALL (p) { REMOVE p:Dormant } IN TRANSACTIONS OF 10000 ROWS;
