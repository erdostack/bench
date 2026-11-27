// ticket: ENT-77 withdraw the 2027 entries whose fee was not paid by 15 Nov 2026; bursary entries stay (docs/entry-rules.md)
// count before/after: MATCH (e:Entry:Entered) WHERE e.year = 2027 AND e.feePaid = false AND e.bursary = false RETURN count(e);
MATCH (e:Entry:Entered)
WHERE e.year = 2027 AND e.feePaid = false AND e.bursary = false
CALL (e) {
  SET e:Withdrawn
} IN TRANSACTIONS OF 1000 ROWS;
