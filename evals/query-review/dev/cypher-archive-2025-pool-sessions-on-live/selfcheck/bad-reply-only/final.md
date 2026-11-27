Not run: live is production. Here is what to put in changes/OPS-512-archive-2025-sessions.cypher:

```cypher
MATCH (s:Session) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') AND s.programme <> 'school'
CALL (s) { SET s:ArchivedSession REMOVE s:Session } IN TRANSACTIONS OF 5000 ROWS;
```
Check it with EXPLAIN first.