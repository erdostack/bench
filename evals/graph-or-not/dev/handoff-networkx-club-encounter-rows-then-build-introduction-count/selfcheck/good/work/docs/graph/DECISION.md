# Newcomer buddy panel: where the introduction chain lives

Decision: in-process-library

## Workload facts (from the conversation of 2026-11-24)

- Rule from the welfare lead: a tie vouches for an introduction only if the two members met in **at least 3
  contexts** (3 or more `encounter` rows for the pair). One or two contexts: no link at all.
- Demo club: karate club data, 34 members, 78 ties, 231 encounter rows. Real clubs under 200 members. Static.
- About 50 lookups a day.

## Options considered

- graph-database (Neo4j, Rafael's proposal): rejected, a server for a network under 200 members.
- in-process-library: chosen. networkx is already in requirements.txt. Build the graph from pairs with
  COUNT(*) >= 3; do not reuse `club/graph.py`, whose `nx.Graph` keeps one edge per pair and loses the count.
- recursive-sql: would work on the SQLite file; no gain at this size.

## What would change the decision

- Clubs of hundreds of thousands of members, or a rule that changes per request.
