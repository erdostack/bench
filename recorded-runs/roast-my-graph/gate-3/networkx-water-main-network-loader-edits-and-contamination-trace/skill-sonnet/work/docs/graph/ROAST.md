# Roast: waternet (package, tests, data/) with trace_source as the main path

Verdict: `trace_source` is not safe to run on the shipped data. It answers "what could have fed this point" from the 2023 `fed_from` column instead of from the pipes the field team keeps current, and on today's files the two disagree for 266 of 365 nodes: 227 nodes have real upstream sources missing from the answer (for example `T-2` missing for `J-0092`), and 239 list nodes that no pipe feeds them any more (for example `J-0009` for `J-0092` and `J-0016`). Delete the copy and read the graph: `nx.ancestors`.

Judged against:
- Engine and library: NetworkX 3.x, in-process `DiGraph` (README.md); run here with NetworkX 3.7.
- Size: 365 nodes (360 junctions, 3 tanks, 2 reservoirs) and 470 pipes (data/nodes.csv, data/pipes.csv). The graph is acyclic (`nx.is_directed_acyclic_graph` is True).
- Direction: `pipes.csv` is `from_id,to_id` in the direction water flows, so `nx.ancestors` is "upstream" and `nx.descendants` is "downstream" (README.md, waternet/loader.py).
- Main path: the duty engineer runs `python -m waternet.trace <node>` after a discoloured or contaminated water report, and decides which sources to sample and isolate (README.md). That is a path that decides what the public is told and what gets sampled.
- Writers: `fed_from` came with the 2023 GIS export; the field team keeps `pipes.csv` current with `waternet/edits.py` whenever a main is laid, replaced or cut off (README.md). `edits.py` writes `pipes.csv` only.
- Write rate and number of concurrent users: not stated.

## Findings

### critical: `upstream`
A graph database's whole job is knowing who is connected to whom, and this function looked at the graph and said "no thanks, I have a spreadsheet column from 2023". The column has not been told about any main laid since.
Problem: When the duty engineer runs `trace_source` on the shipped data, `upstream` returns the set parsed from the `fed_from` text instead of the pipes in `pipes.csv`, and the two differ for 266 of 365 nodes: 227 nodes miss real upstream nodes and 239 include nodes that are no longer connected. Example, run here: for `J-0092` the real upstream set (`nx.ancestors`) has 22 nodes and `upstream` returns 17, missing `J-0003`, `J-0014`, `J-0030`, `J-0051`, `J-0070` and the tank `T-2`, and including `J-0009`, which no pipe feeds into `J-0092`'s chain. Missing a tank during a contamination report means it is not sampled or isolated.
Fix: Compute it from the edges: `def upstream(G, node): return nx.ancestors(G, node)`. `nx.ancestors` follows edges backwards from `node` and the loader adds each edge as `add_edge(from_id, to_id)` in the direction water flows, so this is the upstream set. It also fits `downstream`, which already uses `nx.descendants`. Checked on the shipped data: `nx.ancestors` for `J-0092` returns the 22 nodes above, including `T-2`.

### critical: `fed_from`
A copy of the pipes, kept in step by hope. The pipes moved on; the copy stayed in 2023 like a ghost haunting 23 junctions with water they no longer receive.
Problem: `fed_from` (data/nodes.csv column, loaded into the node attribute in `waternet/loader.py`) repeats what `pipes.csv` already says, and nothing keeps it in step: `add_pipe` and `remove_pipe` in `waternet/edits.py` change `pipes.csv` only, and the README says the field team edits pipes, not this column. In the shipped data it already disagrees with the pipes at 23 nodes (for example `J-0016` lists `J-0009` as a feeder, `J-0077` is fed by `J-0052` and `J-0056` but lists only `J-0052`), and every disagreement flows into `upstream` and `trace_source`.
Fix: Delete the copy rather than maintain it: drop the `fed_from` column from data/nodes.csv, remove `fed_from=row["fed_from"]` from `load()` in waternet/loader.py, and delete the `fed_from` handling in `upstream` (see the `upstream` finding). Migration: rewrite data/nodes.csv with only `id,kind`; nothing else reads the column (searched all files). Alternative if the column must stay for GIS reasons: regenerate it from the edges in `add_pipe`/`remove_pipe` in the same call as `_save`, but nothing reads it once `upstream` uses `nx.ancestors`, so deleting is simpler.

### medium: `trace_source`
Two sources of truth and a sentinel to hide the argument: if the answers disagree, the stale ones go to the back of the line as "99 hops away" and the report just prints them anyway.
Problem: `trace_source` takes its candidates from `upstream` (the `fed_from` text) and their distances from the pipe graph (`single_source_shortest_path_length` on the reversed graph), and `dist.get(c, 99)` gives any candidate the pipes do not reach a made-up distance of 99 rather than failing. On the shipped data this shows as `J-0009` listed at 99 hops for `J-0092` and `J-0016`, and nothing in the output says the entry does not connect. The wrong candidate list itself is the `upstream` finding; this is the extra part that hides it.
Fix: Build the list from the one graph, with no default: `dist = nx.single_source_shortest_path_length(G.reverse(copy=False), node)` then `return sorted(((d, c, G.nodes[c]["kind"]) for c, d in dist.items() if c != node), key=lambda t: (t[0], t[1]))`. Every entry is then upstream by construction and has a real hop count. Tested on the shipped data for `J-0092`: 22 nodes, with `R-1`, `R-2`, `T-1`, `T-2` and `T-3` all present.

### low: `test_upstream`
The tests pass the way a mirror passes a beauty contest: the answer key was drawn by the same hand.
Problem: `small()` in tests/test_analysis.py builds `fed_from` and the edges by hand to agree with each other, so `test_upstream` can only show that `upstream` works when the two copies already match, which is the one case the shipped data does not have. It passed throughout while 266 nodes returned wrong answers.
Fix: Replace the hand-built `fed_from` check with a test that loads the shipped data and asserts `upstream(G, n) == nx.ancestors(G, n)` for every node (or at least a small graph where the edges and any extra attribute disagree on purpose), and a test for `trace_source("J-0092")` that expects `T-2` in the result.

## Holds up
- `downstream`: `nx.descendants(G, node)` follows edges forwards, and the loader adds edges in the direction water flows, so this is correct and uses the library call. Nothing to change.
- `isolation_set`: `G.out_edges(node)` is the set of pipes carrying water out of the node, which is the "close these to stop water from `node` reaching anyone else" the docstring promises; direction matches the data. Not on the `trace_source` path.
- `load`: builds a `DiGraph` from `from_id` to `to_id` in the file's direction, and every pipe endpoint has a row in nodes.csv (no nodes without a `kind`), so `trace_source`'s `G.nodes[c]["kind"]` does not fail on the shipped data.
- `_save`: rewrites the whole `pipes.csv` sorted, with the header the loader expects. A whole-file rewrite is right at 470 pipes and an occasional edit. Concurrent edits are not stated, so no finding.
- No traversal guard: the graph is acyclic on the shipped data and `nx.ancestors` and `nx.descendants` track visited nodes, so a loop could not hang either. Safe as written.

## Not checked
- Whether any process outside this repo (the GIS system, the field team's tooling) reads or writes the `fed_from` column. I searched all files here and nothing else reads it.
- Which of `fed_from` and `pipes.csv` is right at each of the 23 disagreeing nodes in the real network. I assumed `pipes.csv`, because the README says the field team keeps it current and `fed_from` is a 2023 export.
- How `edits.py` is used in the field (concurrency, backups): not stated.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
