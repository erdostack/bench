Position: keep

We decided on recursive-sql. Since the fix the query runs at 4 ms p95 against a 100 ms budget, on 10M tickets and
3M links, and loops can no longer make it run away.
