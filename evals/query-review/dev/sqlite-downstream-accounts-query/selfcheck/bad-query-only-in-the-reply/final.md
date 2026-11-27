Here is the query, I was not sure where you wanted it:

```sql
WITH RECURSIVE d(account_id) AS (SELECT dst FROM transfers WHERE src = :src UNION SELECT t.dst FROM d JOIN transfers t ON t.src = d.account_id)
SELECT account_id FROM d WHERE account_id <> :src;
```
