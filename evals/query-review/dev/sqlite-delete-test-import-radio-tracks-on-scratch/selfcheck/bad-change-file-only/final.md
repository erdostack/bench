Here's the SQL to run on scratch when you're ready:

```sql
DELETE FROM edges WHERE src IN (SELECT id FROM nodes WHERE kind = 'track' AND import_batch = 'IMP-TEST-1121');
DELETE FROM nodes WHERE kind = 'track' AND import_batch = 'IMP-TEST-1121';
```
