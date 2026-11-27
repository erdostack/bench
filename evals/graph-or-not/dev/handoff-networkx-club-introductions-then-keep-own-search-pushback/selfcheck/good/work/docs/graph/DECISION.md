# "Who can introduce me"

Decision: in-process-library

## Workload facts (from the conversation, 2026-11-23)

- club/intro.py's intro_chain compared with networkx shortest_path on all 561 member pairs of the test data
  (karate club, 34 members, 78 ties): ours is longer than needed on 284 pairs, by up to 5 introductions.
- networkx is already a dependency (club/stats.py); shortest_path takes about 4 microseconds there.
- Largest club about 2,000 members; each club is loaded per request.

## Options considered

- graph-database (Noor): rejected; the wrong chains are a search bug, and a server would not change that.
- in-process-library: chosen; replace the hand-written search with nx.shortest_path.
- recursive-sql: rejected; per-request club graphs are already in memory.
- keep our own search: rejected; it is the defect.

## What would change the decision

- Clubs large enough that loading the ties per request stops being cheap (well past 2,000 members).
