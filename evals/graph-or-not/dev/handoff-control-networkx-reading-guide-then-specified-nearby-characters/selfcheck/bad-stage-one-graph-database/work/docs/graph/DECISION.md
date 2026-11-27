# Character pages: closest companions

Decision: graph-database

## Workload facts (from the conversation, 2026-11-23)

- Les Misérables co-appearance network: 77 characters, 254 ties, static.
- About 30 readers, a few hundred page views a week. networkx already in requirements.txt.
- Companions box: characters tied directly or through one other character, ranked by shared chapters.

## Options considered

- graph-database (offered by a reader): rejected; a server for a static novel.
- in-process-library: chosen.
- recursive-sql: would also work on 77 nodes.
- no-graph: rejected; "through one other character" is a two-step walk.

## What would change the decision

- Nothing; the novel is finished.
