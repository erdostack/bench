// 2026-27 window closed 2026-10-31: lapse players not registered for 2026-27 (docs/registration.md). Players only, coaches are not part of this change.
// About 3,900 players, so it is batched: 900 nodes per transaction (limit 1,000). Needs auto-commit (what bin/reg uses).
// Check first (read only): MATCH (p:Player:Registered) WHERE p.lastSeason < '2026-27' RETURN count(p);
MATCH (p:Player:Registered) WHERE p.lastSeason < '2026-27'
CALL {
  WITH p
  SET p:Lapsed
  REMOVE p:Registered
} IN TRANSACTIONS OF 900 ROWS;
