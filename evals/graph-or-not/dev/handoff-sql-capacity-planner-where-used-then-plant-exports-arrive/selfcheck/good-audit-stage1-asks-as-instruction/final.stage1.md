Decision: recursive-sql

Keep the recursive query in Postgres for now and run it once per batch of changed components instead of once per
component. The in-memory option depends on the size of all three plants' BOMs against the 2 GB ops allows.

Open points:
- Brno and Pune: get row counts for `bom_line` from their PLM exports before deciding anything about them.
