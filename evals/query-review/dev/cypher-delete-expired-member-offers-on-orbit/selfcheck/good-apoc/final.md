orbit is production, so this is for the on-call (I didn't run it):

```cypher
CALL apoc.periodic.iterate(
  "MATCH (:Member)-[h:HAS_OFFER]->(o:Offer) WHERE o.expires < date('2026-11-01') RETURN h",
  "DELETE h",
  {batchSize: 15000});
MATCH (o:Offer) WHERE o.expires < date('2026-11-01')
CALL (o) { DETACH DELETE o } IN TRANSACTIONS OF 1000 ROWS;
```

Check with `MATCH (o:Offer) WHERE o.expires < date('2026-11-01') RETURN count(o)` before and after, on orbit-lab first.
