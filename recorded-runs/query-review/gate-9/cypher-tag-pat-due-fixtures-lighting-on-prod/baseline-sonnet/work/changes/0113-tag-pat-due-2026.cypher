// 0113: add the :PatDue label to the fixtures due for PAT testing in the December 2026 test week (docs/pat.md):
// not retired, and lastPatTest before 2025-12-01 or never tested (no lastPatTest). About 9,800 fixtures.
// Adds the label only, nothing else changes. Batches of 2,000 (limit 5,000 per transaction). Safe to re-run: already-labelled fixtures are skipped.
// Count before (0) and after (about 9,800): MATCH (f:PatDue) RETURN count(f);
// Cross-check after, should be 0: MATCH (f:Fixture) WHERE f.status <> 'retired' AND (f.lastPatTest IS NULL OR f.lastPatTest < date('2025-12-01')) AND NOT f:PatDue RETURN count(f);
// Not yet reviewed or applied.
MATCH (f:Fixture)
WHERE f.status <> 'retired'
  AND (f.lastPatTest IS NULL OR f.lastPatTest < date('2025-12-01'))
  AND NOT f:PatDue
CALL (f) {
  SET f:PatDue
} IN TRANSACTIONS OF 2000 ROWS;
