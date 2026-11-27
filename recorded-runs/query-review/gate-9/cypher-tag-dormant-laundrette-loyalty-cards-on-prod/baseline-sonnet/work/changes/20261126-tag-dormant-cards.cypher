// 20261126: tag dormant cards (last wash before 2025-06-01) with :Dormant so marketing can send the winter win-back mail-out on Friday.
// Cards never used (no lastWashOn) are not dormant and are not matched. Staff cards are tagged like any other card.
// Count before and after (about 41,000 expected after, 0 before): MATCH (c:Card:Dormant) RETURN count(c)
// Check afterwards (should be 0): MATCH (c:Card) WHERE c.lastWashOn < date('2025-06-01') AND NOT c:Dormant RETURN count(c)
// Committed 10,000 rows at a time so the card readers' writes do not time out behind a long transaction.
MATCH (c:Card)
WHERE c.lastWashOn < date('2025-06-01') AND NOT c:Dormant
CALL (c) {
  SET c:Dormant
} IN TRANSACTIONS OF 10000 ROWS;
