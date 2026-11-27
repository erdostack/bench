// 20261126: tag dormant cards with :Dormant for the winter win-back mail-out (goes out Friday 2026-11-27).
// Why: docs/model.md defines :Dormant as a card not used for a wash since before 2025-06-01. A card that has never
// been used (lastWashOn not set) is not dormant, and it does not match here: the comparison is null, so it is skipped.
// Staff cards are tagged like any other card (docs/model.md).
// Batching: 10,000 rows per transaction (docs/changes.md). Run by the loyalty-scheme admin after review:
//   bin/wc prod --file changes/20261126-tag-dormant-cards.cypher
// Language: assumes the database default (docs/graph/CONTEXT.md is not in the repo, so the query_language is unknown).
// Expected count: about 41,000 (docs/model.md). Not counted from the database; this repo has no read access to prod here.
//
// Before (must match the admin's count; note already_tagged, which the run should not change):
//   MATCH (c:Card) WHERE c.lastWashOn < date('2025-06-01') RETURN count(c) AS should_change
//   MATCH (c:Dormant) RETURN count(c) AS already_tagged
// After (should_change + already_tagged, unless some tagged card was washed again during the run):
//   MATCH (c:Dormant) RETURN count(c) AS dormant
//   MATCH (c:Dormant) WHERE NOT c.lastWashOn < date('2025-06-01') RETURN count(c) AS should_not_be_tagged   // expect 0
// Re-runs: SET of an existing label changes nothing, so a second run should change nothing (not tested here).

MATCH (c:Card)
WHERE c.lastWashOn < date('2025-06-01')
CALL (c) {
  SET c:Dormant
} IN TRANSACTIONS OF 10000 ROWS;
