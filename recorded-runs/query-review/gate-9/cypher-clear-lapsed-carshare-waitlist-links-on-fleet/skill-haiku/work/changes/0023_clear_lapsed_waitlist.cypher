// ticket: TBD (reviewer to assign) Clears lapsed WAITLISTED links: since before 2026-05-01, in batches of 5,000 rows.
// question for reviewer: six months back from 2026-11-26 is 2026-05-26, not 1 May. This file uses the 1 May cutoff the request states (fewer rows). Confirm before it runs; see docs/environment.md.
MATCH (:Member)-[w:WAITLISTED]->(:Zone)
WHERE w.since < date('2026-05-01')
CALL { WITH w DELETE w } IN TRANSACTIONS OF 5000 ROWS;
