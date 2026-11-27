# Nightly access review: where the walk runs

Decision: in-process-library

## Workload facts (from the owner, 2026-11-24)

- 38,000 identities, 6,500 groups, 390,000 membership edges. networkx peaks at about 260 MB; the job takes 4
  minutes.
- It must run on review-01, certified by the auditors as it is: 2 GB RAM. A bigger box means re-certification and
  is off the table.
- CISO's rule: while the job fits in review-01's 2 GB it stays as it is; if it ever does not, it moves to the
  licensed graph database on the certified security cluster. No tuning tricks to squeeze it back in.

## Options considered

- graph-database (Hannes): not now; it is the agreed next step if the job stops fitting.
- in-process-library: chosen; it runs today with an eighth of the box.
- recursive-sql: there is no SQL database here; the export is JSON lines.

## What would change the decision

- The job not fitting in 2 GB on review-01: move to the graph database on the security cluster.
