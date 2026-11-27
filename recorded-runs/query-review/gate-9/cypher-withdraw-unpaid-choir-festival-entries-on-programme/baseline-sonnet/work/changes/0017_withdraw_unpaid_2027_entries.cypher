// ticket: ENT-77 withdraw 2027 entries whose fee (due 15 Nov 2026) is unpaid; bursary entries excluded. Needs PR review before the entries secretary runs it.
MATCH (e:Entry:Entered) WHERE e.year = 2027 AND e.feePaid = false AND e.bursary = false
CALL (e) { SET e:Withdrawn REMOVE e:Entered } IN TRANSACTIONS OF 1000 ROWS;
