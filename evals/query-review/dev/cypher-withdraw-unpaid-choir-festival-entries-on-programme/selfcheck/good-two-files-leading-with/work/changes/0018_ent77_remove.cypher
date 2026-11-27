// ticket: ENT-77 withdraw the 2027 entries whose fee was not paid by 15 Nov 2026; bursary entries stay (docs/entry-rules.md)
MATCH (e:Entry:Withdrawn:Entered)
CALL (e) { REMOVE e:Entered } IN TRANSACTIONS OF 1000 ROWS;
