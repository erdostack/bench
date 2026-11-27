Position: keep

- What we decided (ADR 0018): keep the recursive blockers query on Postgres.
- Why it went down: loops in the blocking links (about 1,700 of them) and a query that did not guard against them.
  Each ran to the 30 s timeout.
- That is fixed: since October the query skips tickets already on its path, and it runs at 11 ms p95 against the
  panel's 300 ms.
- A graph database would add a second copy of the links and still need the same guard. Not worth it.
