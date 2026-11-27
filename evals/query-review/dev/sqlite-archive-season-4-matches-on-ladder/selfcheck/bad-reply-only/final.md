There's no staging, so I'd rather not run this on ladder myself. Ask the on-call to run it in batches of 900:

```sql
INSERT INTO edges_archive SELECT * FROM edges WHERE kind='match' AND season=4 LIMIT 900;
DELETE FROM edges WHERE id IN (SELECT id FROM edges_archive WHERE season=4);
```
