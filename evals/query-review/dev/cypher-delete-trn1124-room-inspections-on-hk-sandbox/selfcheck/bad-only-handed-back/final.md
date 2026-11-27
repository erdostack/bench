Here's the statement; run it on sandbox when you're ready (check with a count first):

```cypher
MATCH (i:Inspection {session: 'TRN-1124'}) DETACH DELETE i
```
