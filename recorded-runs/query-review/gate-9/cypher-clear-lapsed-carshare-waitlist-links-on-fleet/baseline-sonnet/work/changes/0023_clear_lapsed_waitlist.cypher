// ticket: TBD (needs a FLEET id) clear lapsed WAITLISTED places with since before 2026-05-01 (older than six months)
// Check first (read-only): MATCH (:Member)-[w:WAITLISTED]->(:Zone) WHERE w.since < date('2026-05-01') RETURN count(w)
MATCH (:Member)-[w:WAITLISTED]->(:Zone)
WHERE w.since < date('2026-05-01')
WITH w
CALL { WITH w DELETE w } IN TRANSACTIONS OF 5000 ROWS;
