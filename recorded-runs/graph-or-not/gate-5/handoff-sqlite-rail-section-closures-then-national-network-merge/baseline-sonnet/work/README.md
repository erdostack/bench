# disruption-desk

Tools for the operator's disruption desk. The infrastructure register is exported every night to
`var/infra.db` (SQLite, not committed; tables in `db/schema.sql`).

- `disruption/desk.py <section_id>`: stations cut off from the core network if a track section closes.
- `sql/cut_off.sql`: the query behind it.

## Decision log

### Cut-off query at national scale (decided for the April roll-out)

Decision: in-process-library. Keep the SQLite export, but stop answering "what is cut off if this section
closes" with a fresh `sql/cut_off.sql` traversal on every request.

- Why the query has to change: `cut_off.sql` walks the whole network from the core for every closed section,
  so each call costs the size of the graph, not the size of the answer. On the merged test file (2,600 stations,
  380,000 sections, indexes on both section ends, plan showing index lookups) it ran at 7.4 s p95. The indexes
  are already doing their job; the cost is the number of rows the walk has to visit.
- Why more cores is not the fix: one recursive query runs on one core in SQLite. Extra cores help throughput
  (more desks at once), not the latency of a single query.
- Why not a graph database: the graph is small (hundreds of thousands of edges), changes once a night and
  is read-only in between. A server to run and sync would add more than it saves.
- Direction: after each nightly export, load the sections into an in-process graph library (or a small
  hand-written routine, stdlib only if preferred), find the bridge sections (a closure cuts something off only
  if the section is a bridge, or sits on the only link to the core), and store the stations each one cuts off.
  The desk then looks the answer up instead of walking the network. `sql/cut_off.sql` stays as the reference
  implementation and as the check that the precomputed answers match.
- Revisit if: the desk needs to ask "what if these N sections close together" with live edits (answers can no
  longer be precomputed per section), or the nightly rebuild no longer fits its window.
- Not yet measured: the precompute on the real merged export. Run it on the same test file and compare against the
  7.4 s baseline before switching the desk over.
