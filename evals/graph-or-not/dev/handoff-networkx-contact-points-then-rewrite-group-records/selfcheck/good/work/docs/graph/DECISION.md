# Customer dedupe grouping

Decision: in-process-library

## Workload facts (from the conversation, 2026-11-23)

- Product's rule: two records are the same person only if they share an email or a phone. A shared address is
  NOT a link (it merged a student hall into one customer).
- Groups are transitive: if A shares an email with B and B a phone with C, A, B and C are one person.
- The current one-pass loop in dedupe/link.py never merges two existing groups: on last week's export, with
  address removed, it gave 480,581 groups; networkx connected_components gave 464,663.
- Export: 640k records, 1.25M contact points. networkx: about 2 s, 560 MB, on the 16 GB batch box. Nightly,
  2 hour window.

## Options considered

- graph-database (vendor pitch): rejected; a server for one nightly batch that runs in seconds in memory.
- in-process-library: chosen; networkx connected_components in the job.
- recursive-sql: rejected; components as a recursive query would carry every reachable id per record.
- no-graph: rejected; transitivity is the point.

## What would change the decision

- A real-time "is this the same customer" lookup at signup, rather than a nightly batch.
