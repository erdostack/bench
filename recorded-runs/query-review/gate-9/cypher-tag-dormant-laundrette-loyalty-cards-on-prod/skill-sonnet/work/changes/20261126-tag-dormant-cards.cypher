// 20261126: tag dormant cards (last wash before 2025-06-01) with :Dormant for Friday's winter win-back mail-out.
// Why: docs/model.md defines :Dormant as a card not washed since before 2025-06-01. Cards never used
// (no lastWashOn) are not dormant, and the comparison below skips them because null < date is null.
// Staff cards are tagged like any other card (docs/model.md). Commits 10,000 cards per transaction
// (docs/changes.md); the statement must run auto-commit (bin/wc --file does), not inside an explicit transaction.
// Safe to run twice: the second run matches nothing, because tagged cards are skipped.
// Written for Neo4j 5.26. CALL (c) { } needs 5.23 or later. Not run anywhere: there is no copy to try it on.
// Question for the reviewer: please EXPLAIN it on prod first (plan only, writes nothing).
// Count before (about 41,000 expected by docs/model.md, not measured): MATCH (c:Card) WHERE c.lastWashOn < date('2025-06-01') RETURN count(c)
// Count tagged before (expect 0): MATCH (c:Card:Dormant) RETURN count(c)
// Count after (must equal the "before" count, plus any card that went dormant during the run): MATCH (c:Card:Dormant) RETURN count(c)
// Check after (expect 0): MATCH (c:Dormant) WHERE c.lastWashOn IS NULL OR c.lastWashOn >= date('2025-06-01') RETURN count(c)
MATCH (c:Card)
WHERE c.lastWashOn < date('2025-06-01') AND NOT c:Dormant
CALL (c) {
  SET c:Dormant
} IN TRANSACTIONS OF 10000 ROWS;
