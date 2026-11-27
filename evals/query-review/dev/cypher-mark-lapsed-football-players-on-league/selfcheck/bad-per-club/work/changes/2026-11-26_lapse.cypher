// lapse club by club
MATCH (c:Club)
CALL (c) {
  MATCH (p:Player:Registered)-[:PLAYS_FOR]->(:Team)-[:OF_CLUB]->(c) WHERE p.lastSeason < '2026-27'
  SET p:Lapsed REMOVE p:Registered
} IN TRANSACTIONS OF 10 ROWS;
