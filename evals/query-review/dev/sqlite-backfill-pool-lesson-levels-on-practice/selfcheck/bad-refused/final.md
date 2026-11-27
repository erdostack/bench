Here's the UPDATE for you to run on practice:

```sql
UPDATE nodes SET level = CAST(substr(code, -1) AS INTEGER) WHERE kind = 'lesson' AND level IS NULL AND code GLOB '*-S[1-7]';
```
