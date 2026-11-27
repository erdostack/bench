Decision: recursive-sql

Keep the citation snapshot in SQLite and replace the search with a bounded, bidirectional, visited-set traversal that runs on the existing indexes. The 41 s comes from how the prototype walks, not from SQLite being the wrong place for this traversal. A graph database or a 53 GB in-memory graph is not needed to meet 3 s.

Why:

- The search space is small when it is searched properly. Each paper has on average about 4.3 outgoing citations (410M over 96M papers), and a search needs chains of up to 6 hops. Expanding from both ends, each side only has to go 3 hops. At average degree that is on the order of a few hundred to a few thousand rows per side, not the 6-hop path enumeration the prototype does.
- The prototype enumerates paths. `sql/path.sql` carries a `path` string per walk and has no visited set across walks, so it generates every simple path up to 6 hops from `:a` before it looks at `:b`. The `ORDER BY hops LIMIT 5` happens after all that work. The same pattern made the path-array query in the other repos blow up on meshed graphs; the cost grows with paths, not papers.
- The `edge` CTE is a `UNION ALL` of both directions. It is likely the planner cannot probe `citation`'s two indexes through it cheaply in the recursive join. That is the first thing to check, with `EXPLAIN QUERY PLAN` on a copy of the snapshot. If it is not using `citation (citing_id, cited_id)` and `citation (cited_id, citing_id)` directly, two explicit joins (one per direction) should fix it.
- Filters belong at each hop, not after the walk. Retraction is `paper.retracted = 0` on the node being added, and the year filter is `paper.year > :X` in the same join. Both are indexed lookups on `paper` by id, with no rebuild. Each new filter is a clause, not a new graph build, which is what took Wen two weeks.
- Daily changes are plain inserts into `citation` and `paper`, the same as the 1.2M new citations a day. No 40-minute rebuild, no closure table to invalidate. The closure table is out, as the request says (about 90 billion rows).
- Why not in-process-library: the numpy adjacency works (6 GB, 0.8 s) and is a real fallback, but it bakes the filters into a rebuild path. The 40-minute daily rebuild and the two-week cost per filter are the reasons the platform team said no. It should be kept only if the SQL version misses on the real snapshot.
- Why not graph-database: the same data and the same indexes already exist in SQLite, and a dedicated graph database adds a second store to refresh daily.

Sketch of the search (for design discussion; untested on the snapshot):

- Expand from `:a` over `citation.citing_id` (out-edges) and from `:b` over `citation.cited_id` (in-edges), one level at a time, keeping a `seen` map with a parent pointer per side.
- At each level, add only nodes that are not retracted and (if given) have year greater than X.
- Stop when the two frontiers meet, or after 6 total hops. Expand the smaller frontier first.
- Rebuild the chains from the parent pointers on both sides, and cap the number returned at 5.

I tested that search shape in SQLite on a synthetic graph of 200,000 papers and about 860,000 citations, with a skewed in-degree (some papers cited much more often than others). Across 300 random pairs, the median search touched 120 rows and the 95th percentile touched 377 (max 1,498), with p95 time about 8 ms. This is a toy graph, and it says nothing about the real snapshot's hubs, so it does not show the 3 s budget is met.

What is not yet known, and the main risk:

- Heavy-tailed hubs. A paper cited tens of thousands of times multiplies the frontier on the next level. The average degree of 4.3 is the right order of magnitude, but the real degree distribution decides p95. This needs a timing on a copy of the 96M-paper snapshot, with a sample of real pairs including hub papers.
- Counting all shortest chains can be exponential through hubs. The cap on returned chains must apply during reconstruction, not after the search.

Next steps:

1. Run `EXPLAIN QUERY PLAN` on the current `sql/path.sql` on the snapshot copy, and confirm whether `edge` uses the citation indexes.
2. Write the bidirectional, visited-set search (level by level, or as a recursive query with a visited set and the two directions as separate joins). Keep both filters in the join.
3. Time it on the snapshot copy with a sample of real pairs, including hubs, and report p50 and p95 against the 3 s budget with 400 users.
4. Only if p95 misses after the SQL rewrite, measure the numpy adjacency against the same sample, and weigh its rebuild and filter costs against a second store.
