# Repeal impact

Decision: graph-database

## Workload facts (from the conversation, 2026-11-23)

- Register: 4,800 bylaws, 21,000 references, SQLite copy refreshed nightly. About a dozen clerks use the page.
- bylaws/impact.py walks one query per level and stops at 3 levels (MAX_LEVELS) because deeper searches timed
  out. Amendment chains are up to 9 deep now, so it misses bylaws.
- networkx: load 0.3 s, any answer under 1 ms.
- City clerk's rule: only `amends` and `depends_on` references carry a repeal. A bylaw that only CITES the
  repealed one is not affected, and nothing is carried through a citation. Any depth.

## Options considered

- graph-database (consultant): rejected; a server for a nightly copy and a dozen users.
- in-process-library: chosen; networkx ancestors over amends/depends_on edges, graph built once per refresh.
- recursive-sql: would also work (a recursive query filtered by kind); networkx chosen because it is one call.
- no-graph: rejected; chains are 9 deep.

## What would change the decision

- Several departments querying the register at the same time with writes, not a nightly copy.
