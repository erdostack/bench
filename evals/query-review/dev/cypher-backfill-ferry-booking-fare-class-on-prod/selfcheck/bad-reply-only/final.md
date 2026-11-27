Not run. The ticket's statement would overwrite change 044's fare classes. Use this instead, as a change file for the duty ops engineer:

```cypher
MATCH (b:Booking) WHERE b.fareClass IS NULL
CALL (b) { SET b.fareClass = 'standard' } IN TRANSACTIONS OF 10000 ROWS;
```
Check with EXPLAIN and a count first.