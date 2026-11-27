# Graph decision

Decision: in-process-library

The lab asked whether the "start here" reading list, which ranks papers by a citation score, needs Neo4j with its graph algorithms, the graph library already installed, recursive SQL on the SQLite file, or no graph at all. The score is PageRank with the PI's damping factor of 0.7 over the whole citation graph, run once a night, so the graph fits in memory in one process and networkx 3.7, already pinned, computes it. The finding it turns on: the citation graph of 4,800 papers and 31,000 edges measured about 6 MB in networkx, and a PageRank run took about 0.56 s (synthetic graph of the same size).

## Workload facts

- 4,800 papers and 31,000 citation rows (stated by the user)
- 610 papers have no references (stated by the user); derived: 610 / 4,800 = 12.7% of papers are dangling nodes with no outgoing citations
- The PI's rule: damping factor 0.7, not the usual 0.85, so that directly cited papers count for more than long chains (stated by the user)
- The reading list is rebuilt nightly and nobody waits on it (stated by the user); no latency budget
- The existing `litmap/score.py` is a hand-written power iteration: `importance(conn, rounds=10, damping=0.85)`, a fixed 10 rounds with no convergence test, and the mass of papers with no references is never redistributed, so the scores do not sum to 1 (`litmap/score.py`, `litmap/reading.py`)
- `litmap/reading.py` takes the top 20 by that score, with a TODO to switch to the ranking the lab decides on (`litmap/reading.py`)
- The schema holds `paper (id, title, year)` and `cites (citing_id, cited_id)` with primary key (citing_id, cited_id); no index on cited_id (`db/schema.sql`)
- networkx 3.7 is pinned in `requirements.txt` and already used by `litmap/plots.py` for the citation graph (`requirements.txt`, `litmap/plots.py`)
- The real database `var/library.db` is rebuilt nightly by `litmap/sync.py`, which is not in the repo; the real counts and the real top-20 comparison are not available (`README.md`)
- Measured (synthetic, same size: 4,800 nodes, 31,000 random directed edges; not the real library): networkx 3.7 on Python 3.13.18, a traced 5.96 MB for the graph, about 192 bytes per edge (`measured`: tracemalloc around the load; nothing written to disk)
- Measured: `nx.pagerank(g, alpha=0.7)` on that graph took about 0.56 s and its scores summed to 1.000000 with 6 nodes that have no outgoing edges (`measured`)
- Derived: edge memory = 31,000 x 192 bytes, about 6 MB per process, well under any memory a small job host would give one process (the host's limit is unknown); one process holds one copy, and the nightly job needs one
- unknown: the real top-20 comparison, since the real database is not in the repo; the 13-paper overlap cannot be explained from the data at hand
- unknown: whether the real graph has more attributes per edge than the bare citation pair; the synthetic run kept none
- unknown: whether the PI wants papers with no references to pass their score on evenly, as networkx does, or to keep their share; the repo does not say, and this is a modelling choice for the PI, not a workload fact

## Options considered

- graph-database (Neo4j with its graph algorithms library, as Jun suggested): rejected, because the job is one whole-graph PageRank over about 6 MB of edges once a night with no latency budget. A server would be a second stateful system to run and feed from the reference-manager export, for an algorithm the library the lab already pins runs in under a second.
- in-process-library (networkx 3.7 already pinned, with the graph loaded in memory for the nightly job): chosen, because the whole citation graph fits comfortably in one process (about 6 MB measured on a same-size synthetic graph), the job is batch and runs over every edge (the shape the heuristics give to this option), and the nightly rebuild meets the freshness the readers need. The PI's damping of 0.7 is passed as `alpha=0.7`; the existing hand-written loop can be retired.
- recursive-sql (recursive queries on the SQLite file): rejected, because PageRank is an iterative algorithm over the whole graph, not a walk from one starting paper; expressing it in SQL would mean repeating a full join over all edges for each round, with no request-time need that would favour it.
- no-graph (plain joins, no traversal): rejected, because the score is defined over the whole citation graph and cannot come from a single join or a lookup per paper.

## What would change the decision

- The citation graph grows to a size where one copy per process no longer fits the job host's memory, measured on the real file with the real attributes; this would be re-examined against the host's limit, which is not in the repo.
- The nightly job stops being a batch run, for example if the reading list must be ranked per request or updated on every new citation; then the choice would be re-examined, and a precomputed table written nightly would still avoid a graph database.
- The real database, when measured, shows a top-20 ranking that differs from the PI's expected list for reasons other than the damping and the handling of papers with no references; then the input data would need checking before any change to the method.
