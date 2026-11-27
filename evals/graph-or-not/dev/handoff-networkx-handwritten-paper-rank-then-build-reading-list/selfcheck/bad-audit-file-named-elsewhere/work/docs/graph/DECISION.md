# Reading list ranking

Decision: in-process-library

## Workload facts (from the conversation of 2026-11-24)

- Library: 4,800 papers, 31,000 citation rows; 610 papers have no references.
- Hand-written score (litmap/score.py) vs nx.pagerank: top 20 share only 13 papers; scores do not sum to 1.
- **PI's rule: damping factor 0.7** (not the default 0.85): directly cited papers should count for more.
- Rebuilt nightly; nobody waits on it.

## Options considered

- graph-database (Neo4j + its algorithms library, Jun): rejected, a server for a nightly batch.
- in-process-library: chosen. nx.pagerank(g, alpha=0.7) on citing -> cited.
- recursive-sql: not a fit for an iterative ranking.

## What would change the decision

- A library of hundreds of millions of citations, or a ranking needed per request.
