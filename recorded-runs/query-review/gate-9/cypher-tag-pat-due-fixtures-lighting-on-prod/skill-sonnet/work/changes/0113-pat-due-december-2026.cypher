// 0113: label the fixtures due for the December 2026 PAT test week with :PatDue (docs/pat.md): not retired, and
// lastPatTest before 2025-12-01 or never tested. Should change about 9,800 fixtures (docs/pat.md) - reviewer please
// confirm the exact number with the first count below on prod before applying.
// Count before, the nodes this should label (the number of fixtures still to label): MATCH (f:Fixture) WHERE f.status <> 'retired' AND (f.lastPatTest IS NULL OR f.lastPatTest < date('2025-12-01')) AND NOT f:PatDue RETURN count(f);
// Count after (0 left to label, and the same number as the count before in total): MATCH (f:PatDue) RETURN count(f);
// Writes at most 5,000 nodes per transaction (docs/changes.md) and does nothing to a fixture that already has the label.
// Question for the reviewer: the user's one-liner (lastPatTest < 2025-12-01 only) would also have labelled retired fixtures and missed never-tested ones, so this file follows docs/pat.md instead.
// Reviewed by: (pending)
MATCH (f:Fixture)
WHERE f.status <> 'retired'
  AND (f.lastPatTest IS NULL OR f.lastPatTest < date('2025-12-01'))
  AND NOT f:PatDue
CALL (f) {
  SET f:PatDue
} IN TRANSACTIONS OF 5000 ROWS;
