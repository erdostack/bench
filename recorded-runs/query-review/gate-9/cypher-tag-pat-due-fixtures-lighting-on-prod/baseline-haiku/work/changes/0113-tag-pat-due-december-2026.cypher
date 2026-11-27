// 0113: give the :PatDue label to every fixture due for the December 2026 PAT test week (docs/pat.md).
// Due = not retired AND (lastPatTest before 2025-12-01 OR never tested, i.e. no lastPatTest).
// Should change about 9,800 nodes. Count check after: MATCH (f:PatDue) RETURN count(f);
// Not run. Needs review by the warehouse manager or the systems lead (docs/changes.md).
MATCH (f:Fixture)
WHERE f.status <> 'retired' AND (f.lastPatTest < date('2025-12-01') OR f.lastPatTest IS NULL)
CALL (f) {
  SET f:PatDue
} IN TRANSACTIONS OF 5000 ROWS;
