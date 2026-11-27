// committee minute <REVIEWER: add minute date or ticket>: the B-list is scrapped, every track on it drops to C. Moves IN_ROTATION B -> C (since = today), 900 tracks (1,800 changes) per transaction; the Rotation B node and the USES_ROTATION links from show clocks stay. Re-running continues where it stopped and does nothing once B is empty. Needs an auto-commit session (CALL ... IN TRANSACTIONS). Untested: no Neo4j here, reviewer please run EXPLAIN and the count first.
MATCH (t:Track)-[r:IN_ROTATION]->(:Rotation {code: 'B'})
MATCH (c:Rotation {code: 'C'})
CALL (t, r, c) {
  CREATE (t)-[:IN_ROTATION {since: date()}]->(c)
  DELETE r
} IN TRANSACTIONS OF 900 ROWS;
