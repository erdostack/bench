// 2026-27 window closed 2026-10-31: lapse players not registered for 2026-27 (docs/registration.md).
// About 3,900 players, changed in batches of 500 so each transaction stays under the 1,000-node limit (docs/operations.md).
MATCH (p:Player:Registered) WHERE p.lastSeason < '2026-27'
CALL {
  WITH p
  SET p:Lapsed
  REMOVE p:Registered
} IN TRANSACTIONS OF 500 ROWS;
