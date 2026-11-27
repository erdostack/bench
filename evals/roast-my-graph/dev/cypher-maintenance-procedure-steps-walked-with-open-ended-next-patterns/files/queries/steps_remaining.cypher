// How many steps are left after the one the technician is on.
MATCH (current:Step {uid: $uid})-[:NEXT*]->(later:Step)
RETURN count(later) AS remaining;
