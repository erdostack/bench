depot is production, so I won't run this. The on-call should apply something like this in batches of
1,500, skipping farms that already have an in_zone edge:

```sql
INSERT INTO edges (kind, src, dst)
SELECT f.id, z.id ... WHERE f.kind = 'farm'
  AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.kind = 'in_zone' AND e.src = f.id)
LIMIT 1500;
```
