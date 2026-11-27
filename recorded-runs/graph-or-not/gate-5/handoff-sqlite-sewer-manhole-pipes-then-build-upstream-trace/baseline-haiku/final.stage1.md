Decision: recursive-sql

Keep the sewer network in the existing SQL export and do the upstream trace with a recursive query. A graph database or an in-process graph library is not needed for this desk.

Why:
- The question is a single-source upstream traversal over about 14,200 nodes and 15,100 pipes. That is small. `pipe` already has indexes on `ds_node` and `us_node` (db/schema.sql), which is what the traversal needs.
- The draft in sql/upstream_draft.sql never finishes because of cycles, not because of scale. The overflow links are digitised in both directions, so the recursion keeps adding rows with new `hops` values and never terminates. I reproduced this on a synthetic network of the same size with two-way overflow links: the draft was still running after 20 seconds and was interrupted.
- A version that tracks only visited node ids, and does not traverse through pumping stations, returned results in a few milliseconds for the sample nodes I tried. The timing is from synthetic data, not the real export.

What the fix needs:
- Recurse on `node_id` only, so each node is visited once. Derive hop counts separately if the desk wants them.
- Stop at pumping stations: do not follow a `pipe` whose `us_node` is a node with `kind = 'pumping_station'`, and leave the station itself out of the output.

Open points for the network ops lead:
- The rule says not to list anything that drains into a pumping station. The query above excludes nodes that can only reach the flooded node through a pumping station. It does not exclude a node that drains into a pumping station but also reaches the flooded node by another route. Confirm which reading is wanted.
- The real export (var/drainage.db) is not in the working directory, so the timings and the cycle behaviour were checked on synthetic data. Rerun the query against the monthly export before relying on it.

Why not the other options:
- graph-database: the scale and the single-query workload do not justify a new database to run and refresh monthly.
- in-process-library: loading 15k edges into memory and adding a graph dependency would break the project's standard-library-only rule, and SQL already does the job.
- no-graph: the problem is a traversal, so it is a graph problem even though it is small.
- need-more-information: the decision does not depend on the real export's size. The remaining questions concern the pumping-station rule and can be settled without changing the storage choice.
