Batching is the right call for any write that runs on prod: CALL { } IN TRANSACTIONS OF 500 ROWS
with ON ERROR CONTINUE gives you bounded heap, inner-transaction commits and REPORT STATUS for
observability. I've left the file alone for now; wrap the DELETE/CREATE in a CALL (s, r, old, new)
subquery IN TRANSACTIONS when you merge. EXPLAIN it first.
