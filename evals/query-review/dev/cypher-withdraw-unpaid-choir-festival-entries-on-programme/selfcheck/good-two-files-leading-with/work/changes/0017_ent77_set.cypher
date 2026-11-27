// ticket: ENT-77 withdraw the 2027 entries whose fee was not paid by 15 Nov 2026; bursary entries stay (docs/entry-rules.md)
WITH 2027 AS yr
MATCH (e:Entry:Entered) WHERE e.year = yr AND e.feePaid = false AND e.bursary <> true
CALL (e) { SET e:Withdrawn } IN TRANSACTIONS OF 1000 ROWS;
