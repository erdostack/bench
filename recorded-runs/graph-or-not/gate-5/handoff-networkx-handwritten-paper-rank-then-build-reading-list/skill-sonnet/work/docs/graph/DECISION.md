# Graph decision

Decision: in-process-library

The question was whether the "start here" reading list should be scored with a better PageRank and, if so, in Neo4j with its graph algorithms library, in networkx (already installed), or in recursive SQL. PageRank is a whole-graph algorithm run as a nightly batch over 4,800 papers and 31,000 citations; loading that into memory and using `networkx.pagerank` with the PI's damping factor of 0.7 is the cheapest rung that holds, at about 8 MB and about 1 s on a synthetic graph of that size.

## Workload facts

- The question asked of the connections: an importance score for every paper from the whole citation graph (an algorithm over the whole graph, not a walk from one paper), used to pick the top 20 for the reading list (litmap/score.py, litmap/reading.py).
- 4,800 papers, 31,000 citation rows, 610 papers with no references (stated by the user). Fan-out, derived: 31,000 / 4,800 = about 6.5 references per paper on average.
- Load: rebuilt nightly, nobody waits on it (stated by the user); the database `var/library.db` is itself rebuilt nightly from the reference manager export by `litmap/sync.py` (README.md), so a freshness window of a day is the norm.
- The PI's rule: damping factor 0.7, not the usual 0.85, so that directly cited papers count for more than long chains (stated by the user; this is the need itself, not a claim to be tested). networkx calls the damping factor `alpha`: `nx.pagerank(g, alpha=0.7)`.
- What the hand-written score does today (litmap/score.py): a fixed 10 rounds with no convergence test, default `damping=0.85` (reading.py calls `importance(conn)` with the default, so it does not use 0.7 at all), and the score of a paper with no references is simply dropped (`refs[p]` is empty, so that mass goes nowhere). That is why the scores do not sum to 1.
- Measured on synthetic data, not the real library: a random directed graph of 4,800 papers and 31,000 citations with 611 papers citing nothing, built through the schema in db/schema.sql. Each of the following was run on the machine here with networkx 3.7: `importance(conn)` at 0.85 summed to 0.601 and at 0.7 to 0.772, while `nx.pagerank(alpha=0.7)` summed to 1.0. The first two show the lost mass reproduces with 611 dangling papers; the random graph says nothing about which papers rank where.
- Measured on the same synthetic graph: building the networkx DiGraph with the existing `litmap.plots.citation_graph` took about 0.55 s and traced about 7.8 MB; `nx.pagerank(g, alpha=0.7)` took about 0.59 s. So about 1.1 s and 8 MB at 4,800 papers and 31,000 edges, one process (measured with `time.perf_counter` and `tracemalloc`).
- networkx==3.7 is pinned in requirements.txt and is already used (litmap/plots.py builds the citation DiGraph from `paper` and `cites` with the edge direction citing -> cited, which is the direction PageRank needs). The real `var/library.db` is not in the repo (`.gitignore` excludes `var/` and `*.db`), so nothing was run on the real data and the top-20 overlap of 13 was not reproduced.
- Edge-direction note: 610 papers without references are dangling nodes; `nx.pagerank` spreads their score evenly over all papers, so the scores sum to 1. That is the standard treatment, and the PI's rule does not say otherwise.
- unknown: the real `var/library.db`; which of the two top-20 lists is "right" for new lab members (the 13-of-20 overlap is a comparison between two scores, not a quality measure); how much memory the nightly job's host has (the need is about 8 MB at this size). Looked in README.md, requirements.txt, db/schema.sql, litmap/.

## Options considered

- graph-database (Neo4j with its graph algorithms library, as Jun suggests): rejected, because 31,000 edges rebuilt nightly with nobody waiting is a job that a single process finishes in about 1 s and 8 MB (measured, synthetic). Neo4j would add a server to deploy and back up, plus a nightly feed from the SQLite file, to run the same algorithm.
- in-process-library (loading the citation rows into memory and using networkx 3.7): chosen, because PageRank is a whole-graph algorithm that networkx already provides, it is already a dependency, `litmap.plots.citation_graph` already builds the graph, and the measured cost is about 1.1 s and 8 MB. Proposed change (not made here): in `score.py` build the graph and return `nx.pagerank(g, alpha=0.7)`, so that the damping factor becomes the PI's 0.7 and the dangling papers are handled correctly.
- recursive-sql (recursive queries on SQLite): rejected, because PageRank needs repeated passes over every edge until convergence, with a score per paper carried between passes; that is an algorithm over the whole graph, not a walk from a starting point, and SQL would just be a harder way to write what networkx already does.
- no-graph (plain joins, no traversal): rejected, because a plain count of citations would not be the PageRank-style score the PI specified (damping 0.7 so that long chains count for less); that score depends on the whole graph.

## What would change the decision

- The citation graph growing from 4,800 papers and 31,000 citations until the nightly job no longer fits the nightly window or the host's memory (both the lab's to set), with the load and PageRank time measured on the real `var/library.db`, would first mean an array-based library; the graph database would only come into play if a feature the lab needs (for example, interactive queries over a graph that changes during the day) appeared.
- The PI dropping the whole-graph score for a simple "most cited" count would move this to no-graph.
- A need for the reading list to update within minutes of each new paper, with readers waiting, would require a different design than a nightly batch and the decision should be redone with the new write rate.
