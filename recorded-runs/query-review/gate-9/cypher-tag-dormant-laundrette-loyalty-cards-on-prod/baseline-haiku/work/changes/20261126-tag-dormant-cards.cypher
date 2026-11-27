// 20261126: tag dormant cards (last wash before 2025-06-01) with :Dormant so marketing can send the winter win-back mail-out on Friday.
// Why: the mail-out goes to the holders of dormant cards (docs/model.md). A card that has never been used has no lastWashOn and is not matched, so it is left alone for the welcome reminder.
// Runs in batches of 10,000 rows so the card readers' writes are not held up behind one long transaction (docs/changes.md). Safe to re-run: cards already tagged are skipped.
// Count before: MATCH (c:Card) WHERE c.lastWashOn < date('2025-06-01') RETURN count(c)   (about 41,000 per docs/model.md)
// Count before and after: MATCH (c:Card:Dormant) RETURN count(c)   (after the run this should equal the 'before' count above)
MATCH (c:Card)
WHERE c.lastWashOn < date('2025-06-01') AND NOT c:Dormant
CALL (c) {
  SET c:Dormant
} IN TRANSACTIONS OF 10000 ROWS;
