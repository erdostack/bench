# Decision: ADR 014

Decision: in-process-library

In memory, yes; as the ADR describes it, no.

## Workload facts

- The ADR counted tables (310,400, with 1.93 million edges). Impact analysis is column level: 21.4
  million columns x 18.1 upstream columns on average = about 387 million edges.
- The loading note measured 1.3 GB for 2,000,000 edges in NetworkX, so the ADR's design needs about
  250 GB per pod. The pods have a 4 GiB limit and there are six.
- Freshness is 60 seconds; events peak at 1,400 a second; the ADR reloads every 30 minutes.
- Recursive SQL today: 44% cancelled at 60 s.

## Options considered

- NetworkX in every pod, reloaded every 30 minutes (ADR 014): rejected on the numbers above.
- A graph database: would work; a new product to run.
- Recursive SQL: failing.
- One lineage service on the highmem-64 pool, chosen: edges as two sorted integer arrays (about 6 GB for
  387 million edges, attributes looked up in PostgreSQL by edge id when a reviewer opens one), loaded
  once and then kept current by applying lineage events continuously from the collector's stream, so
  the 60-second rule is met. The six API pods call it.

## What would change the decision

- The service falling behind 1,400 events a second, or needing a second writer: then a graph database.
