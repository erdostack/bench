// ticket: ENT-77 withdraw 2027 entries unpaid after the 15 Nov 2026 fee deadline, excluding bursary entries. DRAFT: not yet reviewed, not run.
MATCH (e:Entry:Entered) WHERE e.year = 2027 AND e.feePaid = false AND e.bursary = false
CALL (e) { SET e:Withdrawn REMOVE e:Entered } IN TRANSACTIONS OF 1000 ROWS;
