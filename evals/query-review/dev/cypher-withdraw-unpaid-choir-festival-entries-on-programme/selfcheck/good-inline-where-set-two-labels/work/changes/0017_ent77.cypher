// ticket: ENT-77 withdraw the 2027 entries whose fee was not paid by 15 Nov 2026; bursary entries stay (docs/entry-rules.md)
MATCH (e:Entry:Entered WHERE e.year = 2027 AND e.feePaid = false AND coalesce(e.bursary, false) = false)
CALL (e) { SET e:Entry:Withdrawn REMOVE e:Entered } IN TRANSACTIONS OF 1000 ROWS;
