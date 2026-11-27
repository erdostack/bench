// same as last year
MATCH (p:Player:Registered) WHERE p.lastSeason < '2026-27'
SET p:Lapsed
REMOVE p:Registered;
