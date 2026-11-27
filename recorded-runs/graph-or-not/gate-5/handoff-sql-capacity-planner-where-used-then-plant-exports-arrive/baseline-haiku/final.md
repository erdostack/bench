Decision: recursive-sql

Keep the where-used traversal in the existing SQL database. The recursive query in `sql/where_used.sql` already walks the BOM upward from a component, and the schema already has the `bom_line_component` index it needs. Loading the BOM into networkx inside the planner is what produced the 1.4 GB and 3-minute run, so the planner should stop doing that.

Evidence: I timed the recursive query on a synthetic BOM of 1.2M lines and 400,000 items, in SQLite in memory with the schema's index. It took about 3 ms per component, so all 40,000 components would take roughly 2 minutes. This is a synthetic shape, not the real Brno, Pune and Linz data, and it ran on SQLite rather than the Postgres 16 that production uses. Re-time on Postgres with the real BOMs before relying on the number. Per-component cost depends on BOM depth and fan-out, and the real data may differ.

Caveats:
- The `UNION` in the recursive query removes duplicates and stops cycles. Keep it as `UNION`, not `UNION ALL`, or a cyclic BOM would loop forever.
- The rest of the planning run calls `retime` for each assembly, so the total run time may depend more on retiming than on this query.

Where it is written down: I added the decision as a bullet in `/run/work/README.md`. I found no other decision record in the work directory.
