// 2026-27 window closed 2026-10-31: lapse players not registered for 2026-27 (docs/registration.md).
// About 3,900 players (docs/model.md, 2026-11-25): batched, 500 per transaction, under the 1,000 nodes-per-transaction limit (docs/operations.md).
// Re-run safe: a lapsed player no longer matches :Registered, so a second run changes nothing.
MATCH (p:Player:Registered) WHERE p.lastSeason < '2026-27'
CALL (p) {
  SET p:Lapsed
  REMOVE p:Registered
} IN TRANSACTIONS OF 500 ROWS;
