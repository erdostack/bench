// lapse
MATCH (p:Player:Registered) WHERE p.lastSeason < date('2026-09-01')
CALL (p) { SET p:Lapsed REMOVE p:Registered } IN TRANSACTIONS OF 1000 ROWS;
