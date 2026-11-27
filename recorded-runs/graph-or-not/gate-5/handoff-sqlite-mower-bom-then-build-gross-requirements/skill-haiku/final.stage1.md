Decision: recursive-sql

Gross requirements for an order can stay in Postgres as one recursive query. The walk is at most 11 levels deep, and each line's quantity is multiplied by 1.04 for scrap on the way down, so the scrap compounds per path as the planning lead asked. The 0.4 s you measured on the biggest mower is well inside the 3 s budget, which leaves room for about 7 times more work per run.

- A graph database would add a second copy of the BOM to keep in step with the nightly PLM copy, and the consultant's claim that MRP is a graph problem does not change the arithmetic: it is a product along each path, summed per part.
- The naive recursive query returns one row per path, and in my synthetic test those rows were close to the distinct parts reached, so it repeats little work. A per-level version gave the same totals, so either can be used.
- Before this ships, check two things. The walk must exclude the order's own depth-0 row, or the order item's quantity is added to the totals. And the `sql/` file uses `:name` placeholders, which SQLite accepts but psycopg does not, so confirm it runs on Postgres through `planning/sqlfile.py`.

Still to find out: how many paths and distinct parts the real Postgres copy produces for the worst order, and whether the scrap also applies to the order's own top-level line. The full evidence, the options considered and what would change the decision are in `docs/graph/DECISION.md` in the working directory. Nothing else in the repo was changed.
