// 0113: give the :PatDue label to every fixture due for the December 2026 PAT test week (docs/pat.md). Not reviewed yet.
// Due: not retired (status is null or not 'retired') and either has no lastPatTest or lastPatTest before 2025-12-01. Never tested fixtures count as due.
// Should change: about 9,800 fixtures (docs/pat.md). Take the exact number on prod before applying with: MATCH (f:Fixture) WHERE (f.status IS NULL OR f.status <> 'retired') AND (f.lastPatTest IS NULL OR f.lastPatTest < date('2025-12-01')) AND NOT f:PatDue RETURN count(f)
// Check after, the first count should equal the number of due fixtures and the second should be 0: MATCH (f:PatDue) RETURN count(f) and MATCH (f:PatDue) WHERE f.status = 'retired' RETURN count(f)
// Re-running changes nothing: fixtures that already have the label are not matched again. Batches of 5,000 nodes per transaction (docs/changes.md).
MATCH (f:Fixture)
WHERE (f.status IS NULL OR f.status <> 'retired')
  AND (f.lastPatTest IS NULL OR f.lastPatTest < date('2025-12-01'))
  AND NOT f:PatDue
CALL (f) {
  SET f:PatDue
} IN TRANSACTIONS OF 5000 ROWS;
