// ticket: ENT-77 withdraw the 2027 entries whose fee was not paid by 15 Nov 2026; bursary entries stay (docs/entry-rules.md)
MATCH (e:Entry) WHERE e:Entered AND e.year = 2027 AND NOT e.feePaid AND NOT e.bursary
CALL { WITH e SET e:Withdrawn } IN TRANSACTIONS OF 500 ROWS;
MATCH (e:Entry:Entered:Withdrawn) WHERE e.year = 2027
CALL { WITH e REMOVE e:Entered } IN TRANSACTIONS OF 500 ROWS;
