# Graph decision

Decision: need-more-information

The question is whether finding the bus operators near a street works permit needs a graph database, an in-process graph library, recursive SQL, or no graph at all. The answer turns on how far "near the works" reaches, which neither the request nor the repo says: one step out is a plain indexed self-join, a fixed two or more steps is a short walk that can stay in the SQLite database, and only an unbounded walk over the whole network points to an in-process library. No depth appears in any file, so the decision cannot be made yet.

## Workload facts

- Network size: 52,000 segments (stated by the user); 47,000 junctions (stated by the user); refreshed weekly (stated by the user).
- Permit rate: about 400 permits per week (stated by the user), about 57 per day (400 / 7), so calls are few and not high-rate.
- Average junction degree: 2 x 52,000 / 47,000 = 2.21 segment ends per junction (derived from the figures above; assumes each segment has two junction ends, as db/schema.sql gives j1 and j2). The mean hides the tail, which is unknown.
- Adjacency: a segment's neighbours are the segments sharing j1 or j2 (db/schema.sql, indexes segment_j1 and segment_j2). Each hop is segment to segment, a relation between things of the same kind. The number of adjacency pairs is the sum over junctions of C(degree, 2): unknown without the degree distribution.
- Depth required: unknown. "Near the works" is not defined in the request (TODO in permits/notify.py), the README, or the schema.
- Current query: none. permits/notify.py `operators_to_notify` raises NotImplementedError and sql/ is empty, so the question the connections will be asked is not yet written.
- Route rows: segment_route holds one row per (segment, operator, route) (db/schema.sql). Their count is unknown.
- Engine: SQLite, per README.md (var/streets.db). Version: unknown.
- Data file: not present. var/ is gitignored and absent from the working copy, so no row count, plan or timing could be measured (measured: none; no commands were run against data).
- Memory: bytes per edge in any in-memory graph is unknown; no sample exists in the repo. Memory per process for a full copy is therefore unknown.
- Freshness: the network reloads weekly (stated by the user). The freshness a permit notice needs is unknown.
- Latency budget and batch window for notifications: unknown.
- Processes that would hold a copy: unknown.
- unknown: required depth; the query that will be written; SQLite version; the data file; route row count; degree distribution and tail fan-out; notification latency budget; number of processes.

## Options considered

- graph-database (a dedicated graph store): rejected on present evidence, because no measurement shows SQL failing at any depth and no depth is stated as deep or online; a 52,000-segment network does not by itself need a second storage engine.
- in-process-library (the edges loaded into memory): not chosen yet. It fits only if the required walk is unbounded or whole-network. The edge list is small, but no bytes-per-edge measurement exists, so memory per process is unverified.
- recursive-sql (recursive queries on the database already run): not shown to hold, because nothing was measured. It is the candidate for a short fixed walk on SQLite with the indexes in db/schema.sql, to be checked once the depth and data are known.
- no-graph (plain joins, no traversal): holds only if the depth is one step, that is, the segments sharing a junction with the works segment, which is a single indexed self-join followed by segment_route. Not chosen until the depth is known.

## What would change the decision

1. Required depth, from the permit policy owner (the highway authority): how many segment hops out from the works count as "near". One hop means no-graph. A fixed two or more hops means recursive-sql, to be measured on SQLite. A whole-network or unbounded reach means in-process-library, loaded from the weekly snapshot, once bytes per edge is measured.
2. The data file: a copy of var/streets.db, or a dump, sent for read-only measurement of row counts, the degree tail, route rows and the reachable set at the depth in (1). A reachable set at that depth that stays small keeps recursive-sql; one that covers most of the network points to in-process-library.
3. Notification latency: how soon after a permit the operators must be told. A batch window of hours fits either recursive-sql or in-process-library; a per-request answer in well under a second favours recursive-sql with the indexes in place.
4. graph-database would move here only if the required reach is deep and online, the reachable sets are large per request, and SQLite is measured failing at that depth with the failure count and its total. Nothing in the present evidence shows this.

Nothing in the repo was changed beyond this file.
